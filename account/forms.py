from django import forms
from .models import Address, CreditCard

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip_code')

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ('card_number', 'holder_name', 'expiration_date')
        widgets = {
            'expiration_date': forms.SelectDateWidget,
        }
