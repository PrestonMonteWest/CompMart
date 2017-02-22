from django import forms

class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class CheckoutForm(forms.Form):
    cvv = forms.CharField(label='CVV', max_length=3)

    def __init__(self, *args, **kwargs):
        cards = kwargs.pop('cards')
        addresses = kwargs.pop('addresses')

        super().__init__(*args, **kwargs)
        self.fields['card'] = forms.ChoiceField(
            choices=[(card.pk, card) for card in cards],
            widget=forms.RadioSelect
        )
        self.fields['address'] = forms.ChoiceField(
            choices=[(address.pk, str(address).upper()) for address in addresses],
            widget=forms.RadioSelect
        )

    def clean_cvv(self):
        cvv = cleaned_data['cvv']

        if not cvv.isdigit():
            raise forms.ValidationError('CVV must be numeric.')

        if len(cvv) != 3:
            raise forms.ValidationError('CVV must be 3 digits long.')

        return cvv
