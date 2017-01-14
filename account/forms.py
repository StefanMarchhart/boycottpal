from django.contrib.auth.forms import AuthenticationForm
from django import forms


# Defines a login form, which allows for login
class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()
