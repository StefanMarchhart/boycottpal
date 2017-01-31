from django.contrib.auth.forms import AuthenticationForm
from django import forms
from account.models import Token


# Defines a login form, which allows for login
from account.models import BoycottUser


class ChangeEmailForm(forms.ModelForm):
    old_email = forms.CharField(label="Old Email")
    email = forms.CharField(label="New Email")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BoycottUser
        fields = ['email']

    def clean(self):
        user=self.user
        cleaned_data = super(ChangeEmailForm, self).clean()
        old_email = self.cleaned_data.get('old_email')
        email = self.cleaned_data.get('email')


        if not old_email or (user.email != old_email):
            raise forms.ValidationError("Your old email is incorrect")

        return cleaned_data


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    password = forms.CharField(label="New Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BoycottUser
        fields = ['password']

    def clean(self):
        user=self.user
        cleaned_data = super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        password = self.cleaned_data.get('password')


        if not old_password or (user.check_password(old_password) == False):
            raise forms.ValidationError("Your old password is incorrect")

        if len(password) < 8:
            raise forms.ValidationError("Your new password must be at least 8 characters long.")

        # At least one letter and one non-letter
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("Your password must contain at least one letter and at least one digit or" \
                                        " punctuation character.")

        return cleaned_data


class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    class Meta:
        model = BoycottUser
        fields = ['password']

    def clean(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Your password must be at least 8 characters long.")

        # At least one letter and one non-letter
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("Your password must contain at least one letter and at least one digit or" \
                                        " punctuation character.")

class TokenForm(forms.Form):
    email = forms.CharField(label="Email")

    def clean(self):
        email = self.cleaned_data.get('email')
        for user in BoycottUser.objects.all():
            if user.email == email:
                return
            else:
                pass
        raise forms.ValidationError("This email isn't associated with an account. Perhaps you mistyped it?")




class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()

class UserForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
    class Meta:
        model = BoycottUser
        fields = ['username', 'email']


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

        if len(password1) < 8:
            raise forms.ValidationError("Your password must be at least 8 characters long.")

        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError("Your password must contain at least one letter and at least one digit or" \
                                        " punctuation character.")


        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user