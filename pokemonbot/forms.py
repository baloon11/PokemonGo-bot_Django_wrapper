from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password2'].label = 'confirmation'
        self.fields['password2'].help_text = ''

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password',
                               max_length=10,
                               widget=forms.PasswordInput())


class SettingsForm(forms.ModelForm):

    class Meta:
        model = UserSettings
        fields = [
            'user',
            'google_email',
            'google_password',
            'location_lon',
            'location_lat',
            'gmapkey'
        ]
        widgets = {
            'user' :forms.HiddenInput(),
            'google_password':forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
