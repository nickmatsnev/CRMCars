# coding=utf-8
from django.template.defaulttags import register


@register.filter(name='my_lookup')
def my_lookup(key):
    if key == [0]:
        return "Не найдено"
    if key == [0, 0]:
        return "Не найдено"
    if key == None or key == '':
        return "Не найдено"
    if key == []:
        return "Сведений не найдено"
    if key == 0:
        return "Нарушений не найдено"
    if key == True:
        return "Отсутствует"
    return key
