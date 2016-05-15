from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Hospital, Doctor
from .forms import HospitalForm, UserForm, DoctorProfileForm


def index(request):
    hospital_list = Hospital.objects.all()
    doctor_list = Doctor.objects.order_by('-likes')[:5]

    context_dict = {'hospitals': hospital_list, 'doctors': doctor_list}
    return render(request, 'med/index.html', context_dict)

def add_hospital(request, hospital_name_slug):
    if request.method == 'POST':
        form = HospitalForm(reqeust.POST)
        if form.is_valid():
            hos = form.save(commit=True)
            return index(request)
        else:
            print (form.errors)
    else:
        form = HospitalForm()

    return render(request, 'med/add_hospital.html', {'form': form})

def profile(request, profile_name):
    user = request.user
    if request.method == 'POST':
        print("sosi")
        user_form = UserForm(data=request.POST, instance=request.user)
        profile_form = DoctorProfileForm(data=request.POST, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            print(profile_name)
            return HttpResponseRedirect('med/profile/{0}/'.format(profile_name))

        else:
             print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm(instance = user)
        profile_form = DoctorProfileForm(instance = user)
    return render(request, 'med/profile.html', {'user_form': user_form, 'profile_form': profile_form})
