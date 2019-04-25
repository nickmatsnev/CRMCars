import json

import django
import requests

from core.lib.constants import *
from portal.models import CacheData


def __do_post(url, data, headers):
    return requests.post(url, data=data, headers=headers)

def __do_post_wo_headers(url, data):
    return requests.post(url, data=data)

def __do_get(url):
    return requests.get(url)



def post(url, data, headers=''):
    if headers=='':
        return __do_post_wo_headers(url,data)
    else:
        return __do_post(url, data, headers)

def get(url):
    return __do_get(url)


