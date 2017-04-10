from django import forms
from django.contrib.auth.models import User
from .models import Hospital, Doctor, Disease, Category


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
    #diseases = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
    #queryset=Disease.objects.all())

    #def __init__(self, *args, **kwargs):
    #    super(DoctorProfileForm, self).__init__(*args, **kwargs)
    #    self.fields['diseases'] = forms.widgets.CheckboxSelectMultiple()
    #    self.fields['diseases'] = Disease.objects.all()
    #    #self.fields['price'] = forms.widgets.CheckboxSelectMultiple()
    #    self.fields['price'] = forms.DecimalField()

    class Meta:
        model = Doctor
        fields = ('hospital', 'category', 'diseases', 'picture')



class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ('name', 'category')
