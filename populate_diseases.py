import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medtech.settings')

def add_disease(name, price):
    disease = DiseaseCategory.objects.get_or_create(name=name, avg_price=price)[0]
    return disease

def populate():
    add_disease('basdthing', 231)
    add_disease('Абсцесс мягких тканей', 200)
    add_disease('Анемия', 2300)
    add_disease('Бурсит', 322)

if __name__ == '__main__':
    django.setup()
    from med.models import DiseaseCategory
    populate()
