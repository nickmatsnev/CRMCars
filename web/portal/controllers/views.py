import ast
import json
import sys

import os

from django.views.decorators.csrf import csrf_exempt

sys.path.append('../')

from portal.controllers.forms import UploadFileForm

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.utils.encoding import smart_text
from core.lib import api_requestor
from core.lib import action_helper
from core.lib import modules
from portal.models import Module
from rest_framework import status




@login_required(login_url="signin")
def clients_list(request):
    items = api_requestor.request('/client/view/')

    return render(request, 'concrete/clients_list.html', {'items': items})


@login_required(login_url="signin")
def users_list(request):
  users = api_requestor.request('/user/')

  return render(request, 'concrete/users_list.html', {'items':users})


@login_required(login_url="signin")
def client_decline(request,id):
    raw_data = api_requestor.request('/client/{0}/view/'.format(id))

    context = {'individual': raw_data['individual'], 'id': raw_data['id'], 'drivers': raw_data['drivers'],
               'history': raw_data['op_history']}

    return render(request, 'concrete/client_decline.html',context)


@login_required(login_url="signin")
def client_scoring(request,id):
    #   res = get_scorista()

    individual_id = api_requestor.request('/client/{0}/view/'.format(id))['individual']['id']

    scoring = api_requestor.request('/individual/{0}/module_data/{1}/'.format(individual_id, "scoring"))['raw_data']

    parameters = api_requestor.request('/individual/{0}/module_data/{1}/'.format(individual_id, "parser_parameters"))[
        'raw_data']

    validate = api_requestor.request('/individual/{0}/module_data/{1}/'.format(individual_id, "parser_validate"))[
        'raw_data']
    val = ast.literal_eval(validate)
    checks = json.dumps(val)
    return render(request, 'concrete/client_scoring.html',
                  {'id': id, 'score': scoring, 'checks': checks, 'raw_data': smart_text(parameters, "utf-8"),
                   'disabled': 'disabled'})

@login_required(login_url="signin")
def source(request):
  return render(request, 'concrete/source.html')


@login_required(login_url="signin")
def client_inspect(request,id):
    raw_data = api_requestor.request('/client/{0}/view/'.format(id))

    context = {'individual': raw_data['individual'], 'id': raw_data['id'], 'drivers': raw_data['drivers'],
               'history': raw_data['op_history'], 'status': raw_data['status'], 'product': raw_data['product'],
               'product_id': raw_data['product_id']}

    return render(request, 'concrete/client_inspect.html', context)


@login_required(login_url="signin")
def accept_client(request, id):
    action_helper.add_action(id, 'scoring_complete_accepted', 'user')
    return redirect("clients_list")


@login_required(login_url="signin")
def reject_client(request, id):
    action_helper.add_action(id, 'scoring_complete_declined', 'user')
    return redirect("clients_list")


@login_required(login_url="signin")
def upload_module(request, module_type):
    if request.method == 'POST':
        response = api_requestor.post_file("/module/%s/upload/" % module_type, request)
        if response.status_code == status.HTTP_202_ACCEPTED:
            return redirect("modules_list", module_type=module_type)
        else:
            return HttpResponse('Some error :(')
    else:
        form = UploadFileForm()
    return render(request, 'concrete/forms/upload_module.html', {'form': form, 'module_type': module_type})


@login_required(login_url="signin")
def parameters_list(request):
    items = api_requestor.request('/module/parser/view/parameters/')

    return render(request, 'concrete/parameters_list.html', {'items': items})


@login_required(login_url="signin")
def products_list(request):
    items = api_requestor.request('/product/view/')

    return render(request, 'concrete/products_list.html', {'items': items})


@login_required(login_url="signin")
def modules_list(request, module_type):
    items = api_requestor.request("/module/%s/view/" % module_type)

    return render(request, 'concrete/modules_list.html', {'module': module_type, 'items': items})


@login_required(login_url="signin")
def product_edit(request, id):
    product = api_requestor.request('/product/{0}/'.format(id))

    if request.method == 'POST':
        patch_data = json.dumps(
            {'primary_scoring': request.POST['primary_scoring'], 'other_scoring': request.POST['other_scoring']})

        response = api_requestor.patch('/product/{0}/'.format(id), patch_data)
        if response.status_code == status.HTTP_200_OK:
            return redirect("products_list")
        else:
            return HttpResponse('Some error :(')

    modules = api_requestor.request('/module/scoring/view/')
    context = {'modules': modules, 'product': product}

    return render(request, 'concrete/forms/product_edit.html', context)


@login_required(login_url="signin")
def product_new(request):

    if request.method == 'POST':
        name = request.POST['name']
        primary_scoring = request.POST['primary_scoring']
        other_scoring = request.POST['other_scoring']

        if primary_scoring == "":
            primary_scoring = 0
        if other_scoring == "":
            other_scoring = 0

        post_data = json.dumps(
            {'name': name,
             'primary_scoring': primary_scoring,
             'other_scoring': other_scoring})

        response = api_requestor.post('/product/', post_data)
        if response.status_code == status.HTTP_201_CREATED:
            return redirect("products_list")
        else:
            return HttpResponse('Some error :(')

    modules = api_requestor.request('/module/scoring/view/')
    context = {'modules': modules, 'product': ''}

    return render(request, 'concrete/forms/product_edit.html', context)
