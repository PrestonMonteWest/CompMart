from django import forms
from django.contrib.auth.models import User

class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100)
