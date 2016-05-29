from django import template
from med.models import Doctor

register = template.Library()

@register.inclusion_tag('med/docs.html')
def get_doctor_list(doc=None):
    return {'docs': Doctor.objects.order_by('-likes')[:5], 'act_doc': doc}
