from django import forms
from django.contrib.auth.models import User
from .models import Hospital, Doctor, Disease, Category, DiseaseAndDoctor
from django.forms import BaseFormSet

class HospitalForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Enter Hospital name.')
    address = forms.CharField(max_length=100, help_text='Enter address')
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Hospital
        fields = ('name', 'address', 'phone_number')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class DoctorProfileForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ('hospital', 'category', 'picture')


class DiseaseAndDoctorForm(forms.ModelForm):

    class Meta:
        model = DiseaseAndDoctor
        fields = ('doctor', 'price', 'disease')


class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ('name', 'category')
