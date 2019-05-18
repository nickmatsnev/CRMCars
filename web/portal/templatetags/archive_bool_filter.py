# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='archive_bool_filter')
def archive_bool_filter(value):
    if value == True:
        return "Да"
    return "Нет"
