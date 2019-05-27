# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='validate_status_loc_filter')
def validate_status_loc_filter(value):
    if value == "Failed":
        return "Следующие проверки не пройдены:"
    if value == "OK":
        return "Проверка пройдена успешно"
    return value
