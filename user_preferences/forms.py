from django import forms

class CurrencyForm(forms.Form):
    currency = forms.CharField(max_length = 4)