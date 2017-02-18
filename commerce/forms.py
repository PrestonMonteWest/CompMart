from django import forms

class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100)
