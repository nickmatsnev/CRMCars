from django.contrib.auth.models import User
from django.contrib.auth.models import *
from django.contrib.auth.forms import *
from django import forms
import json
from django import forms

from portal.models import Product


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UploadFileForm(forms.Form):
    file = forms.FileField()


class UploadClientForm(forms.Form):
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    middle_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    gender = forms.CharField(max_length=10)
    birthday = forms.DateField()

    passport_number = forms.CharField(max_length=20)
    passport_issued_at = forms.DateField()
    passport_issued_by = forms.CharField(max_length=50)
    passport_address_registration = forms.CharField(max_length=50)
    passport_division_code = forms.CharField(max_length=10)
    passport_birthplace = forms.CharField(max_length=30)
    passport_image_1 = forms.FileField()
    passport_image_2 = forms.FileField()
    passport_image_3 = forms.FileField()
    passport_image_4 = forms.FileField()

    driver_license_number = forms.CharField(max_length=10)
    driver_license_issued_at = forms.DateField()
    driver_license_image_1 = forms.FileField()
    driver_license_image_2 = forms.FileField()
