from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'name', 'phone_number', 'product_name', 'product_id', 'product_price', 
            'quantity', 'total_price', 'total_tax', 'total_discount', 'grand_total'
        ]