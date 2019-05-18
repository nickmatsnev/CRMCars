# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='gender_filter')
def gender_filter(value):
    if value == 1:
        return "Мужской"
    return "Женский"
