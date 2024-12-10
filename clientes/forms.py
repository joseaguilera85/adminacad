# clientes/forms.py

from django import forms
from .models import Cliente, Oportunidad, Meeting, Event
from .models import Interaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from datetime import datetime

#----------------------------------------

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'celular', 'mail', 'edad']

#----------------------------------------

class OportunidadForm(forms.ModelForm):
    class Meta:
        model = Oportunidad
        fields = ['project', 'estatus']
        widgets = {
            'estatus': forms.Select(choices=[
                ('prospecto', 'Prospecto'),
                ('en_progreso', 'En Progreso'),
                ('cerrado', 'Cerrado')
            ])}


#----------------------------------------

class CreateOportunidadForm(forms.ModelForm):
    class Meta:
        model = Oportunidad
        fields = ['project']
        
#----------------------------------------
class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['oportunidad','salesperson', 'interaction_type', 'category', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

#----------------------------------------
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#----------------------------------------

from django import forms
from .models import Cliente, Oportunidad, Meeting
from django.contrib.auth.models import User, Group
from datetime import datetime

from django import forms
from django.forms import DateInput, TimeInput
from django.contrib.auth.models import User, Group
from .models import Meeting, Oportunidad
from datetime import datetime

class MeetingForm(forms.ModelForm):
    meeting_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        label='Meeting Date'
    )
    meeting_time = forms.TimeField(
        widget=TimeInput(attrs={'type': 'time'}),
        label='Meeting Time'
    )

    class Meta:
        model = Meeting
        fields = ['client', 'oportunidad', 'salesperson', 'meeting_date', 'meeting_time']

    def __init__(self, *args, cliente_id=None, **kwargs):
        """
        Initialize the form with a custom cliente_id to filter the 'oportunidad' field.
        """
        super().__init__(*args, **kwargs)
        ventas_group = Group.objects.get(name='Ventas')
        self.fields['salesperson'].queryset = User.objects.filter(
            groups=ventas_group,
            is_active=True
        )
        
    def save(self, commit=True):
        """
        Override the save method to combine meeting_date and meeting_time into a single datetime.
        """
        instance = super().save(commit=False)
        
        # Combine date and time fields into a single datetime field
        meeting_datetime = datetime.combine(
            self.cleaned_data['meeting_date'],
            self.cleaned_data['meeting_time']
        )
        instance.date_time = meeting_datetime

        if commit:
            instance.save()
        
        return instance


#---------------------

class EventForm(forms.ModelForm):
    # Add invited clients field with a multiple-choice widget
    invited_clients = forms.ModelMultipleChoiceField(
        queryset=Cliente.objects.none(),  # Filter queryset dynamically in the view
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Invite Clients"
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'invited_clients']
