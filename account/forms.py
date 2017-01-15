from django.contrib.auth.forms import AuthenticationForm
from django import forms


# Defines a login form, which allows for login
from account.models import BoycottUser


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()

class UserForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    class Meta:
        model = BoycottUser
        fields = ['first_name', 'last_name', 'username', 'email']


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')

        for user in BoycottUser.objects.all():
            if user.email == email:
                raise forms.ValidationError("This email is already in use. Perhaps you have an account already?")


        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user