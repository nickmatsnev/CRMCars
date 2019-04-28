import json

import django
import requests
import binascii
import datetime


from core.lib.global_settings import *
from portal.models import CacheData

#Тут запрашиваем информацию с улицы
def __do_post(url, data, headers):
    resp = requests.post(url, data=data, headers=headers)
    return resp.text

def __do_post_wo_headers(url, data):
    resp = requests.post(url, data=data)
    return resp.text

def __do_get(url):
    resp = requests.get(url)
    return resp.text


#тут работаем с БД
def __calculate_crc(input):
    crc = binascii.crc32(input.encode())   & 0xffffffff
    return ('%08X' % crc)


def __set_new_record(type_of_request,crc, url, data='', headers=''):
    if type_of_request == 'POST':
        if headers == '':
            body = __do_post_wo_headers(url,data)
        else:
            body = __do_post(url,data,headers)
    else:
        body = __do_get(url)

    queryset = CacheData.objects.create(type_of_request=type_of_request, url=url, data=data,
                                        headers=headers, crc=crc, body=body, is_active=True, create_time=datetime.datetime.now())
    return queryset


def __get_queryset(type_of_request, url, data='', headers=''):
    crc = __calculate_crc(url + data + json.dumps(headers))
    queryset = CacheData.objects.filter(type_of_request=type_of_request, url=url, data=data,
                                        headers=headers, crc=crc, is_active=True)
    if queryset.count() != 0:
        queryset = queryset.get()

        date_now = datetime.datetime.now().date()
        date_archive = queryset.create_time.date()

        if (date_now-date_archive).days > CACHE_TIMEOUT_DAYS:
            queryset.is_active = False
            queryset.save(update_fields=['is_active'])

            queryset = __set_new_record(type_of_request, crc, url, data, headers)

        if CACHE_ALLWAYS_EXTERNAL == True:
            queryset.is_active = False
            queryset.save(update_fields=['is_active'])
            return __set_new_record(type_of_request, crc, url, data, headers).body
        
        return queryset.body
    else:
        queryset = __set_new_record(type_of_request, crc, url, data, headers)
        return queryset.body


#Тут обрабатываем  запросы
def post_data(url, data):
    return json.loads(__get_queryset('POST', url, data=data))

def post_data_headers(url, data, headers):
    return json.loads(__get_queryset('POST', url, data=data, headers=headers))

def get_data(url):
    return json.loads(__get_queryset('GET', url))


