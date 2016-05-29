from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from .models import Hospital, Doctor
from .forms import HospitalForm, UserForm, DoctorProfileForm


def index(request):
    hospital_list = Hospital.objects.all()
    doctor_list = Doctor.objects.all()

    context_dict = {'hospitals': hospital_list, 'doctors': doctor_list}
    return render(request, 'med/index.html', context_dict)

@login_required
def add_hospital(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            hos = form.save(commit=True)
            return index(request)
        else:
            print (form.errors)
    else:
        form = HospitalForm()

    return render(request, 'med/add_hospital.html', {'form': form})

@login_required
def edit_profile(request):
    user = request.user
    doc_profile = Doctor.objects.filter(user=user).first()
    if request.method == 'POST':
        profile_form = DoctorProfileForm(data=request.POST, instance=doc_profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            return HttpResponseRedirect('/med/profile/')
        else:
             print(profile_form.errors)
    elif doc_profile is not None:
        profile_form = DoctorProfileForm(initial=model_to_dict(doc_profile))
    else:
        profile_form = DoctorProfileForm()
    return render(request, 'med/edit_profile.html', {'profile_form': profile_form, 'doc_profile': doc_profile})

def profile(request, profile_name):
    context_dict = {}
    try:
        doctor = Doctor.objects.get(user__username=profile_name)
        context_dict['doctor'] = doctor
    except Doctor.DoesNotExist:
        pass
    return render(request, 'med/profile.html', context_dict)


def hospital(request, hospital_name_slug):
    context_dict = {}
    try:
        hospital = Hospital.objects.get(slug=hospital_name_slug)
        doctors = Doctor.objects.filter(hospital=hospital).order_by('-likes')
        context_dict['hospital'] = hospital
        context_dict['doctors'] = doctors
    except Hospital.DoesNotExist:
        pass
    return render(request, 'med/hospital.html', context_dict)
