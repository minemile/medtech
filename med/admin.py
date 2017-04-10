from django.contrib import admin
from .models import Hospital, Doctor, Disease, Category, DiseaseAndDoctor

class HospitalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class DiseaseAdmin(admin.ModelAdmin):
    exclude = ('avg_price',)

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Doctor)
admin.site.register(Category)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(DiseaseAndDoctor)
