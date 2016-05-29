from django.contrib import admin
from .models import Hospital, Doctor

class HospitalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Doctor)
