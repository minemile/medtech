from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Hospital, Doctor
from .forms import HospitalForm, DoctorForm, DoctorProfileForm

def index(request):
    hospital_list = Hospital.objects.all()
    doctor_list = Doctor.objects.order_by('-likes')[:5]
    context_dict = {'hospitals': hospital_list, 'doctors': doctor_list}
    return render(request, 'med/index.html', context_dict)
