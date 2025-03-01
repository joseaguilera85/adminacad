from django import forms
from django.forms.widgets import SelectDateWidget
from .models import PriceList
from clientes.models import Cliente, Oportunidad
from django import forms
from django.utils import timezone
from datetime import timedelta


class PaymentPlanForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente')  # Add this field
    porcentaje_descuento = forms.DecimalField(label='% de descuento')
    porcentaje_enganche = forms.DecimalField(label='% de enganche')
    porcentaje_mensualidades = forms.DecimalField(label='% de mensualidades')
    num_mensualidades = forms.IntegerField(label='Número de mensualidades')

    # Get today's date and 2 years later
    today = timezone.now().date()
    two_years_later = today + timedelta(days=2*365)  # Approximate 2 years

    # Customizing the DateField to show only month and year
    mes_inicio = forms.DateField(
        label='Mes de inicio', 
        initial=today,  # Set the initial value to today's date
        widget=SelectDateWidget(
            years=range(today.year, two_years_later.year + 1),  # Year range from this year to 2 years later
            empty_label=("Choose Year", "Choose Month", "")
        )
    )

#--------------------------

class VentaPlanForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Oportunidad.objects.all().select_related('project').order_by('project__name'),
        label='Cliente'
    )  # Add this field
    porcentaje_descuento = forms.DecimalField(label='% de descuento')
    porcentaje_enganche = forms.DecimalField(label='% de enganche')
    porcentaje_mensualidades = forms.DecimalField(label='% de mensualidades')
    num_mensualidades = forms.IntegerField(label='Número de mensualidades')
    porcentaje_descuento = forms.DecimalField(label='% de descuento')
    porcentaje_enganche = forms.DecimalField(label='% de enganche')
    porcentaje_mensualidades = forms.DecimalField(label='% de mensualidades')
    num_mensualidades = forms.IntegerField(label='Número de mensualidades')

    # Get today's date and 2 years later
    today = timezone.now().date()
    two_years_later = today + timedelta(days=2*365)  # Approximate 2 years

    # Customizing the DateField to show only month and year
    mes_inicio = forms.DateField(
        label='Mes de inicio', 
        initial=today,  # Set the initial value to today's date
        widget=SelectDateWidget(
            years=range(today.year, two_years_later.year + 1),  # Year range from this year to 2 years later
            empty_label=("Choose Year", "Choose Month", "")
        )
    )

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Get the project from the kwargs
        super().__init__(*args, **kwargs)

        if project:
            # Filter the 'cliente' queryset based on the project
            self.fields['cliente'].queryset = Oportunidad.objects.filter(project=project)

#--------------------------


class ApartmentSearchForm(forms.Form):
    apartment_number = forms.CharField(label="Apartment Number", max_length=10)


#--------------------------

class PriceListForm(forms.ModelForm):
    class Meta:
        model = PriceList
        fields = ['current_list_price_index', 'list_number_0', 'list_number_1', 'list_number_2', 'list_number_3', 'list_number_4', 'list_number_5']


#-------------------------

from django import forms
from .models import House

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['name', 'color', 'points']  # Only these fields are needed for irregular shapes
        widgets = {
            'points': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': 'Enter coordinates as a list of tuples, e.g., [(20, 20), (30, 30), (50, 50)]'}),
        }


#-----------------
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV", required=True)