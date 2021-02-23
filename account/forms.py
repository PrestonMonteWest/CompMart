import datetime
import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from .models import Address, CreditCard


class MonthYearWidget(Widget):
    '''
    A Widget that splits date input into two <select> boxes for month and year,
    with "day" defaulting to the first of the month.
    '''

    none_value = (0, '---')
    month_field = '%s_month'
    year_field = '%s_year'

    date_re = re.compile(r'(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')

    def __init__(self, attrs=None, years=None, required=True):
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, str):
                match = date_re.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = list(MONTHS.items())
        year_choices = [(i, i) for i in self.years]
        if not self.required:
            month_choices.insert(0, self.none_value)
            year_choices.insert(0, self.none_value)

        local_attrs = self.build_attrs({'id': self.month_field % id_})
        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe('\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == '0':
            return None
        if y and m:
            return '%s-%s-%s' % (y, m, 1)

        return data.get(name)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip_code')


class CreditCardForm(forms.ModelForm):
    number = forms.CharField(label='Card Number', min_length=13, max_length=19)

    class Meta:
        model = CreditCard
        fields = ('holder_name', 'expiration_date')
        widgets = {'expiration_date': MonthYearWidget}

    @staticmethod
    def is_luhn(number):
        if len(number) < 2:
            raise ValueError('Card number is too short.')

        digits = list(map(int, number))
        total = sum(digits[-1::-2])
        even_digits = digits[-2::-2]
        for digit in even_digits:
            digit += digit
            total += (digit if digit <= 9 else digit - 9)

        return total % 10 == 0

    @staticmethod
    def get_card_type(number):
        if number[0] == '4':
            return 'Visa'
        elif number[:2] in ('34', '37'):
            return 'American Express'
        elif number[:2] in ('51', '52', '53', '54', '55'):
            return 'MasterCard'
        else:
            raise forms.ValidationError('Unsupported card entered.')

    def clean_number(self):
        number = self.cleaned_data['number']

        if not number.isdigit():
            raise forms.ValidationError('Card number must be numeric.')

        if not self.is_luhn(number):
            raise forms.ValidationError('Invalid card number entered.')

        return number

    def clean_expiration_date(self):
        exp_date = self.cleaned_data['expiration_date']
        today = datetime.date.today()
        expired = exp_date.year < today.year or (
            exp_date.year == today.year and exp_date.month < today.month
        )

        if expired:
            raise forms.ValidationError('Card is expired.')

        return exp_date

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        if number:
            cleaned_data['card_type'] = self.get_card_type(number)

        return cleaned_data

    '''def save(self, commit=True):
        card = super().save(commit=False)
        card.number = self.cleaned_data['number']

        if commit:
            card.save()

        return card'''


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'email',
        )

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
