from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import User


class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Enter First Name', min_length=4, max_length=50, help_text='Required')
    last_name = forms.CharField(label='Enter Last Name', min_length=4, max_length=50, help_text='Required')
    aadharNumber = forms.CharField(label='Enter aaDharNumber', min_length=16, max_length=16, help_text='Required')

    
    class Meta:
        model = User
        fields = ('email','aadharNumber')

    def clean_aadharNumber(self):
        aadharNumber = self.cleaned_data['aadharNumber'].lower()
        r = User.objects.filter(aadharNumber=aadharNumber)
        if r.count():
            raise forms.ValidationError("aadharNumber already exists")
        return aadharNumber

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email