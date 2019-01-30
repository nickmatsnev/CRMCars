import json

import requests

url = "http://127.0.0.1:8002/api"
headers = {"accept": "application/json", "Content-Type": "application/json",
                "X-CSRFToken": "cs7VEXgiMjC8AkslcgzThx8Mb7daEynFhxpl6UjpquwhePwWhBbZCHKZbbQED28c"}

#returns json
def request(relative_url):
    response = requests.get(url+relative_url, headers=headers)
    return json.loads(response.content.decode('utf-8'))
#    return  response

def post(relative_url,body):
    response = requests.post(url+relative_url, headers=headers, data=body)
    return response

