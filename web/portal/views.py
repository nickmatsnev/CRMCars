import json

import sys



import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import *

from core.lib import api_requestor


@login_required(login_url="signin")
def clients_list(request):
  raw_data = api_requestor.request('/clients/')

  return render(request, 'concrete/clients_list.html', {'title': 'Список заявок','items':raw_data})

@login_required(login_url="signin")
def client_scoring(request):
  return render(request, 'concrete/client_scoring.html', {'title': 'Скоринг клиента'})

@login_required(login_url="signin")
def source(request):
  return render(request, 'concrete/source.html', {'title': 'Ресурс//Source'})


@login_required(login_url="signin")
def client_inspect(request,id):
    raw_data = api_requestor.request('/clients/{0}/'.format(id))

    first_name =  raw_data['individuals'][0]['first_name']
    last_name = raw_data['individuals'][0]['last_name']
    middle_name = raw_data['individuals'][0]['middle_name']

    passport_num = raw_data['individuals'][0]['passport']['number']

    context = {'first_name':first_name,'last_name':last_name,'middle_name':middle_name,'passport_num':passport_num,'id':id}

    return render(request, 'concrete/client_inspect.html',context)




