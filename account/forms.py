from django.contrib.auth.forms import AuthenticationForm
from django import forms


# Defines a login form, which allows for login
from account.models import BoycottUser


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = BoycottUser
