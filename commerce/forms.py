from django import forms

class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
