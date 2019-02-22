import json
import requests
import sys
from django.http.response import HttpResponse

sys.path.append('../../')

from core.lib.global_settings import API_ROOT_URL

headers = {'Content-type': 'application/json'}
def request(relative_url):
    response = requests.get(API_ROOT_URL + relative_url)
    return json.loads(response.content.decode('utf-8'))


def request_no_recode(relative_url):
    response = requests.get(API_ROOT_URL + relative_url)
    return json.loads(response.content)


def post(relative_url,body):
    response = requests.post(API_ROOT_URL + relative_url, data=body, headers=headers)
    # TODO HERE ADD CAPTURING BAD REQUEST AND SUCH SHIT TO THROW EXCEPTION !! IF NOT SUCCESS - ...
    return response


def post_json(relative_url, body):
    response = requests.post(API_ROOT_URL + relative_url, json=body)
    # TODO HERE ADD CAPTURING BAD REQUEST AND SUCH SHIT TO THROW EXCEPTION !! IF NOT SUCCESS - ...
    return response

def patch(relative_url, body):
    response = requests.patch(API_ROOT_URL + relative_url, data=body, headers=headers)
    # TODO HERE ADD CAPTURING BAD REQUEST AND SUCH SHIT TO THROW EXCEPTION !! IF NOT SUCCESS - ...
    return response

def post_file(relative_url, request):
    file = request.FILES['file']
    files = {'file': file.open()}
    response = requests.post(API_ROOT_URL + relative_url,files=files)
    # TODO HERE ADD CAPTURING BAD REQUEST AND SUCH SHIT TO THROW EXCEPTION !! IF NOT SUCCESS - ...
    return response


def post_decode(relative_url,body):
    response = requests.post(API_ROOT_URL + relative_url, data=body)
    return json.loads(response.content.decode('utf-8'))