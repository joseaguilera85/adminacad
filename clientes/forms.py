# clientes/forms.py

from django import forms
from .models import Cliente, Project, Meeting
from .models import Interaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from datetime import datetime

#----------------------------------------

class ClienteForm(forms.ModelForm):
    # Add user-related fields to the form    
    class Meta:
        model = Cliente
        fields = ['project', 'nombre', 'apellido', 'edad', 'celular', 'mail', 'modo_contacto', 'estatus', 'tipo_propiedad']
        widgets = {
            'modo_contacto': forms.Select(choices=[('redes', 'Redes'), ('fisico', 'Fisico')]),
            'estatus': forms.Select(choices=[('lead', 'Lead'), ('cliente', 'Cliente'), ('inactivo', 'Inactivo')]),
            'tipo_propiedad': forms.Select(choices=[('terreno', 'Terreno'), ('departamento', 'Departamento'), ('casa', 'Casa')]),
        }


#----------------------------------------
class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['interaction_type', 'category', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

#----------------------------------------
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#----------------------------------------

class MeetingForm(forms.ModelForm):
    # Add separate fields for date and time
    meeting_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Meeting Date')
    meeting_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Meeting Time')

    class Meta:
        model = Meeting
        fields = ['client', 'salesperson', 'meeting_date', 'meeting_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter salespersons to only active users in the "Ventas" group
        ventas_group = Group.objects.get(name='Ventas')  # Get the Ventas group
        self.fields['salesperson'].queryset = User.objects.filter(
            groups=ventas_group,
            is_active=True
        )

    def save(self, commit=True):
        # Save the meeting instance with the combined date and time
        instance = super().save(commit=False)
        # Combine the date and time into the date_time field
        meeting_datetime = datetime.combine(self.cleaned_data['meeting_date'], self.cleaned_data['meeting_time'])
        instance.date_time = meeting_datetime

        if commit:
            instance.save()
        return instance
