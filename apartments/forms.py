from django import forms
from .models import Apartment, Project
from django.forms.widgets import DateInput
import datetime

#-------------------------

class ProjectForm(forms.ModelForm):
    start_date = forms.DateField( widget=forms.DateInput(attrs={'type': 'date', 'value': datetime.date.today().strftime('%Y-%m-%d')}), label='Start Date' )

    class Meta:
        model = Project
        fields = ['name', 'location', 'start_date','tipo', 'description']

#-------------------------

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [ 'project','number', 'area', 'tipologia','points']  # Include 'project' in the fields
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),  # Add a dropdown for project
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }



#-------------------------
class UploadFileForm(forms.Form):
    file = forms.FileField()

#-------------------------


class UploadFileForm(forms.Form):
    file = forms.FileField()
