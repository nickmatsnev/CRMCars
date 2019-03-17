import os
import uuid
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag(filename='status_menu.html')
def status_menu(statuses):
    return {'status_list': statuses}
