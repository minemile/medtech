from django import forms
from django.contrib.auth.models import User
from .models import Hospital, Doctor

class HospitalForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text = 'Enter Hospital name.')
    address = forms.CharField(max_length=100, help_text = 'Enter address')
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Hospital
        fields = ('name', 'address')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('price', 'picture', 'hospital')
