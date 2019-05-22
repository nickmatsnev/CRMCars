# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='user_active_loc_filter')
def user_active_loc_filter(value):
    if value == True:
        return "Действующий"
    if value == False:
        return "Отключен"
    return value
