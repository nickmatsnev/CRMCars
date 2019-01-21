import json

import sys



import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import *
from django.utils.encoding import smart_text

from core.lib import api_requestor
from core.scoring.scorista import get_scorista, get_scoring, get_checks


@login_required(login_url="signin")
def clients_list(request):
  raw_data = api_requestor.request('/clients/')
  items = []
  for elem in raw_data:
      elem['individuals'][0]['fio'] = elem['individuals'][0]['first_name'] + ' ' + elem['individuals'][0]['last_name']
      elem['individuals'][0]['created_at'] = elem['created_at']
      items.append(elem['individuals'][0])

  return render(request, 'concrete/clients_list.html', {'items': items})

@login_required(login_url="signin")
def users_list(request):
  users = User.objects.all()

  return render(request, 'concrete/users_list.html', {'items':users})


@login_required(login_url="signin")
def client_scoring(request,id):
    res = get_scorista()
    score = get_scoring(res)
    checks = get_checks('3333','4444',res)
    return render(request, 'concrete/client_scoring.html',
                  {'id': id, 'score': score, 'checks': checks, 'raw_data': smart_text(res, "utf-8")})

@login_required(login_url="signin")
def source(request):
  return render(request, 'concrete/source.html')


@login_required(login_url="signin")
def client_inspect(request,id):
    raw_data = api_requestor.request('/clients/{0}/'.format(id))
    individual = raw_data['individuals'][0]
    license = raw_data['individuals'][0]['driver_license']
    passport_images = individual['passport']['passport_images']
    license_images = license['driver_license_images']

    context = {'individual': individual, 'license': license, 'passport_images': passport_images,
               'license_images': license_images, 'id': id}

    return render(request, 'concrete/client_inspect.html',context)




