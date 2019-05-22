# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='module_loc_filter')
def module_loc_filter(value):
    if value == "ScoristaParserModule":
        return "Скориста"
    if value == "InfosferaParserModule":
        return "Инфосфера"
    if value == "NBKIParserModule":
        return "НБКИ"
    if value == "ConturFocusParserModule":
        return "Контур-Фокус"
    return value
