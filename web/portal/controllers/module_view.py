import ast
import json
import sys
import io
from time import sleep

from xlsxwriter.workbook import Workbook
import os

from django.views.decorators.csrf import csrf_exempt

sys.path.append('../')

from portal.controllers.forms import UploadFileForm

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.utils.encoding import smart_text
from core.lib import basic_api_requestor
from core.lib import action_helper
from core.lib import modules
from portal.models import Module
from rest_framework import status
from portal.lib.api_requestor import *


@login_required(login_url="signin")
def upload_module(request, module_type):
    if request.method == 'POST':
        response = do_module_upload(module_type,request)
        if response.status_code == status.HTTP_202_ACCEPTED or response.status_code == status.HTTP_201_CREATED:
            return redirect(NAME_MODULES_LIST, module_type=module_type)
        else:
            return HttpResponse(RESPONSE_ERROR)
    else:
        form = UploadFileForm()
    return render(request, URL_LINK_UPLOAD_MODULE, {'form': form, 'module_type': module_type})


@login_required(login_url="signin")
def parameters_list(request):
    items = get_module_parser_parameters()
    return render(request, URL_LINK_PARAMETERS_LIST, {'items': items})


@login_required(login_url="signin")
def products_list(request):
    items = get_product_info()

    return render(request, URL_LINK_PRODUCTS_LIST, {'items': items})


@login_required(login_url="signin")
def modules_list(request, module_type):
    items = get_module_view(module_type)
    return render(request, URL_LINK_MODULES_LIST, {'module': module_type, 'items': items})


@login_required(login_url="signin")
def product_edit(request, id):
    product = get_product(id)

    if request.method == 'POST':
        patch_data = json.dumps(
            {'primary_scoring': request.POST['primary_scoring'], 'other_scoring': request.POST['other_scoring']})

        response = patch_product(id,patch_data)
        if response.status_code == status.HTTP_200_OK:
            return redirect(NAME_PRODUCTS_LIST)
        else:
            return HttpResponse(RESPONSE_ERROR)

    modules = get_scoring_view()
    context = {'modules': modules, 'product': product}

    return render(request, URL_LINK_PRODUCT_EDIT, context)


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

        response = post_product(post_data)
        if response.status_code == status.HTTP_201_CREATED:
            return redirect(NAME_PRODUCTS_LIST)
        else:
            return HttpResponse(RESPONSE_ERROR)

    modules = get_scoring_view()
    context = {'modules': modules, 'product': ''}

    return render(request, URL_LINK_PRODUCT_EDIT, context)
