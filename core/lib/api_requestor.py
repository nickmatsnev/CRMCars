import json

import requests

from lib.global_settings import API_ROOT_URL

headers = {"accept": "application/json", "Content-Type": "application/json",
                "X-CSRFToken": "cs7VEXgiMjC8AkslcgzThx8Mb7daEynFhxpl6UjpquwhePwWhBbZCHKZbbQED28c"}


def request(relative_url):
    response = requests.get(API_ROOT_URL + relative_url, headers=headers)
    return json.loads(response.content.decode('utf-8'))


def post(relative_url,body):
    response = requests.post(API_ROOT_URL + relative_url, headers=headers, data=body)
    return response


def post_decode(relative_url,body):
    response = requests.post(API_ROOT_URL + relative_url, headers=headers, data=body)
    return json.loads(response.content.decode('utf-8'))