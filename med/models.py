from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=100, unique = True)
    address = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User)
    hospital = models.ForeignKey(Hospital)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
