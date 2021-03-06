from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict, inlineformset_factory

from .models import Hospital, Doctor, Disease, DiseaseAndDoctor
from .forms import DoctorProfileForm, DiseaseAndDoctorFormset
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'med/index.html'
    context_object_name = 'doctors_list'

    def get_queryset(self):
        return Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['hospitals_list'] = Hospital.objects.all()
        return context


class DoctorProfileView(generic.DetailView):
    template_name = 'med/doctor_detail.html'
    context_object_name = 'doctor'
    model = Doctor

    def get_object(self, queryset=None):
        return Doctor.objects.get(user__username=self.kwargs['profile_name'])

    def get_context_data(self, **kwargs):
        context = super(DoctorProfileView, self).get_context_data(**kwargs)
        context['dis_and_doc'] = DiseaseAndDoctor.objects.filter(doctor=self.object)
        return context


class DiseaseView(generic.UpdateView):
    template_name = 'med/disease_detail.html'
    context_object_name = 'disease'
    model = Disease
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(DiseaseView, self).get_context_data(**kwargs)
        dis_and_doc = DiseaseAndDoctor.objects.filter(disease=self.object)
        sort_by_price = self.request.POST.get('sort_price')
        sort_by_likes = self.request.POST.get('sort_likes')
        if sort_by_price is not None:
            dis_and_doc = dis_and_doc.order_by("-doctor__likes")
        elif sort_by_likes is not None:
            dis_and_doc = dis_and_doc.order_by("-price")
        else:
            dis_and_doc = dis_and_doc.order_by("-price", "-doctor__likes")
        context['dis_and_doc'] = dis_and_doc
        return context


class CreateHospital(generic.CreateView):
    template_name = 'med/create_hospital.html'
    model = Hospital
    fields = ('name', 'address', 'phone_number')


class HospitalView(generic.DetailView):
    template_name = 'med/hospital_detail.html'
    context_object_name = 'hospital'
    model = Hospital

    def get_object(self, queryset=None):
        return Hospital.objects.get(slug=self.kwargs['hospital_name_slug'])

    def get_context_data(self, **kwargs):
        context = super(HospitalView, self).get_context_data(**kwargs)
        context['doctors_list'] = Doctor.objects.filter(hospital=self.object).order_by('-likes')
        return context


class CreateDiseaseView(generic.CreateView):
    template_name = 'med/create_disease.html'
    context_object_name = 'disease_form'
    fields = ('name', 'category')
    model = Disease


@login_required
def edit_profile(request):
    user = request.user
    doc_profile = Doctor.objects.filter(user=user).first()
    dis_queryset = Disease.objects.all()
    if doc_profile.category:
        dis_queryset = dis_queryset.filter(category=doc_profile.category)
    fs = inlineformset_factory(Doctor, DiseaseAndDoctor, fields=('disease', 'price', 'doctor'), extra=1,
                               can_delete=True, formset=DiseaseAndDoctorFormset)
    disease_n_price = fs(instance=doc_profile, dis_queryset=dis_queryset)
    if request.method == 'POST':
        profile_form = DoctorProfileForm(data=request.POST, instance=doc_profile)
        formset = fs(data=request.POST, instance=doc_profile, dis_queryset=dis_queryset)
        if profile_form.is_valid() and formset.is_valid():
            dis_and_doc = formset.save(commit=False)
            for del_dis in formset.deleted_objects:
                del_dis.delete()
            formset.save()
            for dis in dis_and_doc:
                dis.disease.save()
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
        disease_n_price = fs(instance=doc_profile, dis_queryset=dis_queryset)
    return render(request, 'med/edit_profile.html',
                  {'profile_form': profile_form, 'doc_profile': doc_profile, 'disease_n_price': disease_n_price})


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
    dis_list = Disease.objects.none()
    starts_with = starts_with.lower()
    if starts_with:
        dis_list = Disease.objects.filter(name__icontains=starts_with)
    if max_results > 0 and dis_list:
        if dis_list.count() > max_results:
            dis_list = dis_list[:max_results]
    return dis_list


def suggest_disease(request):
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    dis_list = get_disease_list(8, starts_with)
    return render(request, 'med/dis.html', {'diss': dis_list})
