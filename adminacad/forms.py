# forms.py
from django import forms
from .models import Calificacion


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class CalificacionForm(forms.ModelForm):
    calif_1B = forms.DecimalField(label='Calificación 1B', initial=0)
    calif_2B = forms.DecimalField(label='Calificación 2B', initial=0)
    calif_3B = forms.DecimalField(label='Calificación 3B', initial=0)
    calif_4B = forms.DecimalField(label='Calificación 4B', initial=0)
    calif_5B = forms.DecimalField(label='Calificación 5B', initial=0)

    class Meta:
        model = Calificacion
        fields = ('calif_1B', 'calif_2B', 'calif_3B', 'calif_4B', 'calif_5B')

