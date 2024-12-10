#---------------------------

# Import necessary modules for the User Registration form
from django import forms
from django.contrib.auth.models import User, Group
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    # Define form fields for password and group
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ChoiceField(choices=[('Ventas', 'Ventas'), ('Administracion', 'Administracion')])

    class Meta:
        model = User
        # Include the necessary fields for registration
        fields = ['email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        # Create or update a user instance
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Use email as the username
        user.set_password(self.cleaned_data['password'])  # Set the user's password securely
        
        if commit:
            # Save the user instance to the database
            user.save()
            # Create a corresponding UserProfile
            UserProfile.objects.create(user=user, nombre=user.first_name, apellido=user.last_name)
            
            # Assign the user to a group based on the selected choice
            group_name = self.cleaned_data['group']
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        
        return user

#---------------------------

# Import necessary modules for the Client Registration form
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from clientes.models import Cliente

class ClienteRegistrationForm(forms.ModelForm):
    # Form fields for selecting a client and entering password information
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.none(), label="Select Client")
    password = forms.CharField(widget=PasswordInput, label="Password")
    password_confirmation = forms.CharField(widget=PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        # Only include the password field for the user
        fields = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Exclude clients who already have associated users (username is the client's email)
        self.fields['cliente'].queryset = Cliente.objects.exclude(
            mail__in=User.objects.values_list('username', flat=True)
        )
        
        # Set autofocus on the client selection field and reorder fields
        self.fields['cliente'].widget.attrs['autofocus'] = True
        self.fields = {
            'cliente': self.fields['cliente'],
            'password': self.fields['password'],
            'password_confirmation': self.fields['password_confirmation'],
        }

    def clean(self):
        # Perform additional validation for password matching
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("The two passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        # Save the selected client and user information
        cliente = self.cleaned_data['cliente']
        user = super().save(commit=False)
        user.username = cliente.mail  # Use the client's email as the username
        user.set_password(self.cleaned_data['password'])  # Securely set the password

        if commit:
            # Save the user instance
            user.save()
            # Create the UserProfile linked to the client
            UserProfile.objects.create(
                user=user,
                nombre=cliente.nombre,
                apellido=cliente.apellido
            )
            # Automatically assign the user to the "Cliente" group
            group, created = Group.objects.get_or_create(name="Cliente")
            user.groups.add(group)
        
        return user

#---------------------------
