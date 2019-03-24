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
from portal.lib.constants import *
from portal.lib.api_requestor import *


@login_required(login_url="signin")
def clients_list(request):
    items = get_client()
    statuses = get_client(URL_CLIENT_METHOD_STATUS)
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses})


@login_required(login_url="signin")
def clients_list_filtered(request, status_filter):
    items = get_client_info(status_filter)
    statuses = get_client(URL_CLIENT_METHOD_STATUS)
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses})


@login_required(login_url="signin")
def users_list(request):
    users = basic_api_requestor.request('/user/')
    return render(request, URL_LINK_USERS_LIST, {'items': users})


@login_required(login_url="signin")
def index(request):
    return render(request, URL_LINK_INDEX)


@login_required(login_url="signin")
def source(request):
    return render(request, URL_LINK_SOURCE)


@login_required(login_url="signin")
def reports(request):
    if request.method == 'POST':
        items = get_client_info(request.POST['status'])
        if items == []:
            return redirect(URL_REPORTS)
        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        # row_headers
        for element in items[0].keys():
            worksheet.write(0, col, element)
            col += 1
        col = 0
        row = 1
        # row_values
        for client in items:
            for value in client.values():
                worksheet.write(row, col, str(value))
                col += 1
            row += 1
            col = 0
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=test.xlsx"
        output.close()
        return response

    statuses = get_client(URL_CLIENT_METHOD_STATUS)
    return render(request, URL_LINK_REPORTS, {'statuses': statuses})

