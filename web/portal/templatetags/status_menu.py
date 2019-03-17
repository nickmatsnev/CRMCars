import os
import uuid
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag(name='menu.html')
def status_menu():
    return {}
