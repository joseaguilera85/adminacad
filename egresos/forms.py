# forms.py
from django import forms
from .models import Egreso, Vendor, PurchaseOrder, PurchaseOrderItem
from django.forms import DateInput

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['empresa', 'persona', 'fiscal_id', 'email', 'telephone', 'address', 'state', 'CP']

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['project', 'empresa', 'order_date', 'status']

    order_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

# Form for creating a PurchaseOrderItem
class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['categoria', 'subcategoria', 'item_name', 'quantity', 'price']