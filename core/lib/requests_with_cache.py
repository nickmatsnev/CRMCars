import json

import django
import requests

from core.lib.constants import *
from portal.models import CacheData

#Тут запрашиваем информацию с улицы
def __do_post(url, data, headers):
    resp = requests.post(url, data=data, headers=headers)
    return json.loads(resp.text)

def __do_post_wo_headers(url, data):
    resp = requests.post(url, data=data)
    return json.loads(resp.text)

def __do_get(url):
    resp = requests.get(url)
    return json.loads(resp.text)


#Тут обрабатываем  запросы
def post_data(url, data):
    return __do_post_wo_headers(url,data)

def post_data_headers(url, data, headers):
    return __do_post(url, data, headers)

def get_data(url):
    return __do_get(url)


