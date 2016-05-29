from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Avg
from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator

class Hospital(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=20, validators=[phone_regex], blank=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Hospital, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class DiseaseCategory(models.Model):
    name = models.CharField(max_length=128)
    avg_price = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        avg_price = Doctor.objects.filter(disease=self).aggregate(Avg('price'))
        super(DiseaseCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User)
    hospital = models.ForeignKey(Hospital, null=1, blank=1)
    disease = models.ForeignKey(DiseaseCategory, null=1, blank=1)
    likes = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def save(self, *args, **kwargs):
        if self.picture:
            image = Img.open(BytesIO(self.picture.read()))
            image.thumbnail((300,300), Img.ANTIALIAS)
            output = BytesIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.picture= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.picture.name, 'image/jpeg', output.getbuffer().nbytes, None)
        super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
