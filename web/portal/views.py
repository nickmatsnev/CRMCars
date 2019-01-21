import json

import sys

sys.path.append('../')

from web.portal.models import *

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
      id = elem['individuals'][0]['id']
      gen = Generation.objects.filter(individual_id=id)[0]
      elem['individuals'][0]['status'] = gen.status

      items.append(elem['individuals'][0])

  return render(request, 'concrete/clients_list.html', {'items': items})

@login_required(login_url="signin")
def users_list(request):
  users = User.objects.all()

  return render(request, 'concrete/users_list.html', {'items':users})


@login_required(login_url="signin")
def client_scoring(request,id):
    res = get_scorista()

    checks = get_checks('4518334452', '77МА051161', res)['checks']
    disabled = ""
    gen = Generation.objects.filter(individual_id=id)[0]

    if gen.status == "Новая":
        gen.status = 'В работе'
        gen.save()

    if gen.status == "Потдверждена" or gen.status == "Отказано":
        disabled = "disabled"
    score = get_scoring(json.dumps({'checks': checks}, indent=4, sort_keys=False, ensure_ascii=True))

    return render(request, 'concrete/client_scoring.html',
                  {'id': id, 'score': score, 'checks': checks, 'raw_data': smart_text(res, "utf-8"),
                   'disabled': disabled})

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

    generation_data = api_requestor.request('/generation/')

    op_history = None
    for element in generation_data:
        if element['individual'] == individual['id']:
            op_history = element



    context = {'individual': individual, 'license': license, 'passport_images': passport_images,
               'license_images': license_images, 'id': id, 'history': op_history}

    return render(request, 'concrete/client_inspect.html',context)


@login_required(login_url="signin")
def accept_client(request, id):
    gen = Generation.objects.filter(individual_id=id)[0]
    gen.status = "Потдверждена"
    gen.save()
    return redirect("clients_list")


@login_required(login_url="signin")
def reject_client(request, id):
    gen = Generation.objects.filter(individual_id=id)[0]
    gen.status = "Отказано"
    gen.save()
    return redirect("clients_list")
