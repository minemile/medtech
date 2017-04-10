from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg
from django.core.validators import RegexValidator


class Hospital(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=20, validators=[
                                    phone_regex], blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Hospital, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    CONSULTATION = 'Cons.'
    DIAGNOSTIC = "Diag."
    OPERATIONS = "Oper."
    CATEGORY_TYPES = (
        (CONSULTATION, "Consultation"),
        (DIAGNOSTIC, "Diagnostic"),
        (OPERATIONS, "Operations"),
    )
    name = models.CharField(max_length=128)
    type_category = models.CharField(
        max_length=6, choices=CATEGORY_TYPES, default=CONSULTATION)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=128)
    avg_price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, related_name='diseases')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User)
    hospital = models.ForeignKey(Hospital)
    category = models.ForeignKey(Category)
    diseases = models.ManyToManyField(
        Disease, through='DiseaseAndDoctor', blank=1, related_name='doctor_diseases')
    likes = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class DiseaseAndDoctor(models.Model):
    doctor = models.ForeignKey(Doctor)
    disease = models.ForeignKey(Disease)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
