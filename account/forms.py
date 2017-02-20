from django import forms
from datetime import date
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

    @staticmethod
    def is_luhn(card_number):
        if len(card_number) < 2:
            raise ValueError('Card number is too short.')

        digits = list(map(int, card_number))
        total = sum(digits[-1::-2])
        even_digits = digits[-2::-2]
        for digit in even_digits:
            digit += digit
            total += (digit if digit <= 9 else digit - 9)

        return total % 10 == 0

    @staticmethod
    def get_card_type(card_number):
        if card_number[0] == '4':
            return 'Visa'
        else:
            raise forms.ValidationError('Unsupported card type entered.')

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']

        if not card_number.isdigit():
            raise forms.ValidationError('Card number must be numeric.')

        if len(card_number) < 15 or len(card_number) > 16:
            raise forms.ValidationError('Invalid number of digits entered.')

        if not self.is_luhn(card_number):
            raise forms.ValidationError('Invalid card number entered.')

        return card_number

    def clean_expiration_date(self):
        exp_date = self.cleaned_data['expiration_date']
        today = date.today()
        expired = exp_date.year < today.year or (
            exp_date.year == today.year and exp_date.month < today.month
        )

        if expired:
            raise forms.ValidationError('Card is expired.')

        return exp_date

    def clean(self):
        cleaned_data = super().clean()
        card_number = cleaned_data.get('card_number')
        if card_number:
            cleaned_data['card_type'] = self.get_card_type(card_number)

        return cleaned_data
