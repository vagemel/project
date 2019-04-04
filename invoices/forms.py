from django import forms

from .models import Invoice, Debtor


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = ('user', 'sum')