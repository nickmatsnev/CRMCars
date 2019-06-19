# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='status_color_filter')
def status_color_filter(value):
    if value == "Одобрено":
        return "#B2FEB6;"
    if value == "Отказано до скоринга":
        return "#FE7F7F;"
    if value == "Отказано":
        return "#FE7F7F;"
    if value == "Ожидает согласования":
        return "#FCB161;"
    if value == "Новая":
        return "#E5C8F1;"
    return "#DEDEDE;"
