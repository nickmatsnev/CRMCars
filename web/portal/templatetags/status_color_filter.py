# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='status_color_filter')
def status_color_filter(value):
    if value == "Одобрено":
        return "green;"
    if value == "Отказано до скоринга":
        return "red;"
    if value == "Отказано":
        return "red;"
    if value == "Ожидает согласования":
        return "#E67E22;"
    if value == "Новая":
        return "#6C3483;"

    return "grey;"
