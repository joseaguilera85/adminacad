from django import forms
from .models import BankAccountMovement
from adminacad.models import Student
from django.utils import timezone


class BankAccountMovementForm(forms.ModelForm):
    identificacion = forms.IntegerField()

    class Meta:
        model = BankAccountMovement
        fields = ['identificacion','transaction_date','transaction_type', 'amount', 'description']

        widgets = {
            'transaction_date': forms.DateInput(attrs={'value': timezone.now().date()})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identificacion'].queryset = Student.objects.all()