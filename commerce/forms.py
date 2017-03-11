from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

class MyForm(forms.Form):
    def add_error(self, field, error):
        '''
        Override add_error method in Form,
        so that form doesn't need to be validated to add error.
        '''

        if not isinstance(error, ValidationError):
            error = ValidationError(error)

        if hasattr(error, 'error_dict'):
            if field is not None:
                raise TypeError(
                    "The argument `field` must be `None` when the `error` "
                    "argument contains errors for multiple fields."
                )
            else:
                error = error.error_dict
        else:
            error = {field or NON_FIELD_ERRORS: error.error_list}

        for field, error_list in error.items():
            if field not in self.errors:
                if field != NON_FIELD_ERRORS and field not in self.fields:
                    raise ValueError(
                        "'%s' has no field named '%s'." % (self.__class__.__name__, field)
                    )

                if field == NON_FIELD_ERRORS:
                    self._errors[field] = self.error_class(error_class='nonfield')
                else:
                    self._errors[field] = self.error_class()

            self._errors[field].extend(error_list)
            if hasattr(self, 'cleaned_data') and field in self.cleaned_data:
                del self.cleaned_data[field]

class ProductSearchForm(MyForm):
    query = forms.CharField(max_length=100)

class CheckoutForm(MyForm):
    cvv = forms.CharField(label='CVV', max_length=3)

    def __init__(self, *args, **kwargs):
        if 'cards' not in kwargs:
            raise TypeError("'cards' is required")

        if 'addresses' not in kwargs:
            raise TypeError("'addresses' is required")

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
