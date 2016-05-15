from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Hospital(models.Model):
    name = models.CharField(max_length=100, unique = True)
    address = models.CharField(max_length=100, unique = True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Hospital, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User)
    hospital = models.ForeignKey(Hospital)
    likes = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    specialization = models.CharField(max_length=100, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
