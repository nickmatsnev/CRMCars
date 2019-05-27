# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='report_bool_loc_filter')
def report_bool_loc_filter(value):
    if value == False:
        return "Не найдено"
    if value == True:
        return "Найдено"
    return value
