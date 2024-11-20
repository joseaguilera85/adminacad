from django import forms
from django.contrib.auth.models import User, Group
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ChoiceField(choices=[('Ventas', 'Ventas'), ('Administracion', 'Administracion')])

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
