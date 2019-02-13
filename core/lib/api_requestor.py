import json
import requests
import sys

sys.path.append('../../')

from core.lib.global_settings import API_ROOT_URL


def request(relative_url):
    response = requests.get(API_ROOT_URL + relative_url)
    return json.loads(response.content.decode('utf-8'))


def post(relative_url,body):
    response = requests.post(API_ROOT_URL + relative_url, data=body)
    # TODO HERE ADD CAPTURING BAD REQUEST AND SUCH SHIT TO THROW EXCEPTION !! IF NOT SUCCESS - ...
    return response


def post_file(relative_url, files):
    response = requests.post(API_ROOT_URL + relative_url, files=files)
    # TODO HERE ADD CAPTURING BAD REQUEST AND SUCH SHIT TO THROW EXCEPTION !! IF NOT SUCCESS - ...
    return response


def post_decode(relative_url,body):
    response = requests.post(API_ROOT_URL + relative_url, data=body)
    return json.loads(response.content.decode('utf-8'))