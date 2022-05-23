from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length = 100)

