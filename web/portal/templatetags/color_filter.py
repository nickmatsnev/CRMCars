# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='color_filter')
def color_filter(value):
    if value == "Failed":
        return "red;"
    return "green;"
