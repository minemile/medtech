from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from .models import Hospital, Doctor, Disease
from .forms import HospitalForm, UserForm, DoctorProfileForm, DiseaseForm

from .bing_search import run_query

@login_required
def add_disease(request):
    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease = form.save()

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
            print(form.errors)
    else:
        form = HospitalForm()

    return render(request, 'med/add_hospital.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user
    doc_profile = Doctor.objects.filter(user=user).first()
    if request.method == 'POST':
        profile_form = DoctorProfileForm(
            data=request.POST, instance=doc_profile)
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


def disease(request, disease_name):
    context_dict = {}
    try:
        disease = Disease.objects.get(pk=disease_name)
        doctors = Doctor.objects.filter(disease=disease)
        context_dict['doctors'] = doctors
        context_dict['disease'] = disease
    except Disease.DoesNotExist:
        pass
    return render(request, 'med/disease.html', context_dict)


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


@login_required
def like_doc(request):
    doc_id = None
    if request.method == 'GET':
        doc_id = request.GET['doctor_id']
    likes = 0
    if doc_id:
        doc = Doctor.objects.get(id=int(doc_id))
        if doc:
            likes = doc.likes + 1
            doc.likes = likes
            doc.save()
    return HttpResponse(likes)


def get_disease_list(max_results=0, starts_with=''):
    dis_list = []
    if starts_with:
        dis_list = Disease.objects.filter(
            name__icontains=starts_with)
        print(dis_list)
    if max_results > 0 and dis_list:
        if dis_list.count() > max_results:
            dis_list = dis_list[:max_results]
    return dis_list


def suggest_disease(request):
    dis_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    dis_list = get_disease_list(8, starts_with)
    return render(request, 'med/dis.html', {'diss': dis_list})
