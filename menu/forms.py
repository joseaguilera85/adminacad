from django import forms
from django.contrib.auth.models import User, Group
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ChoiceField(choices=[('Ventas', 'Ventas'), ('Administracion', 'Administracion'),('Cliente', 'Cliente')])

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, nombre=user.first_name, apellido=user.last_name)
            # Assign to group
            group_name = self.cleaned_data['group']
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user

#-----------------------------------------

from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from clientes.models import Cliente

class ClienteRegistrationForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.none(), label="Select Client")
    password = forms.CharField(widget=PasswordInput, label="Password")
    password_confirmation = forms.CharField(widget=PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude clients who already have users
        self.fields['cliente'].queryset = Cliente.objects.exclude(
            mail__in=User.objects.values_list('username', flat=True)
        )
        # Reordering fields
        self.fields['cliente'].widget.attrs['autofocus'] = True
        self.fields = {
            'cliente': self.fields['cliente'],
            'password': self.fields['password'],
            'password_confirmation': self.fields['password_confirmation'],
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("The two passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        cliente = self.cleaned_data['cliente']
        user = super().save(commit=False)
        user.username = cliente.mail  # Use the email from the selected client
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            # Create the UserProfile
            UserProfile.objects.create(
                user=user,
                nombre=cliente.nombre,
                apellido=cliente.apellido
            )
            # Assign the user to the "Cliente" group programmatically
            group, created = Group.objects.get_or_create(name="Cliente")
            user.groups.add(group)
            
        return user

