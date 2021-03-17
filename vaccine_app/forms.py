from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import User, CenterAdmin, DistrictAdmin, DistrictAdmin


class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Enter First Name', min_length=4, max_length=50, help_text='Required')
    last_name = forms.CharField(label='Enter Last Name', min_length=4, max_length=50, help_text='Required')
    aadharNumber = forms.CharField(label='Enter aaDharNumber', min_length=16, max_length=16, help_text='Required')
    center_name = forms.CharField(label='Enter center_name', min_length=0, max_length=30, empty_value="")
    district_name = forms.CharField(label='Enter district_name', min_length=0, max_length=30, empty_value="")
    key = forms.CharField(label='Enter key', min_length=16, max_length=50, help_text='Required')

    class Meta:
        model = User
        fields = ('email','aadharNumber')
    
    def clean_center_name(self):
        return self.cleaned_data['center_name'] or None

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

class ProvideAccessForm(forms.ModelForm):
    center_name = forms.CharField(label='Enter center_name', min_length=0, max_length=30, empty_value="")
    district_name = forms.CharField(label='Enter district_name', min_length=0, max_length=30, empty_value="")
    key = forms.CharField(label='Enter key', min_length=16, max_length=50, help_text='Required')

    class Meta:
        model = DistrictAdmin
        fields = ()
    
    def clean_center_name(self):
        center_name = self.cleaned_data['center_name'].lower()
        if center_name=="_":
            return "_"
        else:
            r = CenterAdmin.objects.filter(name=center_name)
            if r.count()==0:
                raise forms.ValidationError("No Center exists")
        return self.cleaned_data['center_name']
    def clean_district_name(self):
        district_name = self.cleaned_data['district_name'].lower()
        if district_name=="_":
            return "_"
        else:
            r = DistrictAdmin.objects.filter(name=district_name)
            if r.count()==0:
                raise forms.ValidationError("No District exists")
        return self.cleaned_data['district_name']
    