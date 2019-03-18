import ast
import json
import sys
import io

from xlsxwriter.workbook import Workbook
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
    items = api_requestor.request('/client/')
    statuses = api_requestor.request('/client/status/')

    return render(request, 'concrete/clients_list.html', {'items': items, 'statuses': statuses})


@login_required(login_url="signin")
def clients_list_filtered(request, status_filter):
    items = api_requestor.request('/client/{0}/'.format(status_filter))
    statuses = api_requestor.request('/client/status/')

    return render(request, 'concrete/clients_list.html', {'items': items, 'statuses': statuses})


@login_required(login_url="signin")
def users_list(request):
    users = api_requestor.request('/user/')

    return render(request, 'concrete/users_list.html', {'items': users})


@login_required(login_url="signin")
def index(request):
    return render(request, 'index.html')


@login_required(login_url="signin")
def individual_prescoring_decline(request, id):
    raw_data = api_requestor.request('/client/{0}/view/'.format(id))

    context = {'individual': raw_data['individual'], 'id': raw_data['id'], 'drivers': raw_data['drivers'],
               'history': raw_data['op_history']}

    return render(request, 'concrete/client_decline.html', context)


@login_required(login_url="signin")
def individual_scoring(request, id):
    #   res = get_scorista()

    individual_id = api_requestor.request('/individual/{0}'.format(id))
    sources_done = api_requestor.request("/individual/{0}/cur_gen/data/source/".format(id))
    source_names = []
    for item in sources_done:
        source_names.append(item)
    score = api_requestor.request("/individual/{0}/cur_gen/data/scoring/score/".format(id))
    # scoring_data = api_requestor.request('/individual/{0}/cur_gen/data/{1}/'.format(id, "scoring"))
    parser_values = api_requestor.request(
        '/individual/{0}/cur_gen/data/parser/values'.format(id))
    parser_validate_errors = api_requestor.request(
        '/individual/{0}/cur_gen/data/parser/validate/errors'.format(id))
    parser_validate_status = api_requestor.request(
        '/individual/{0}/cur_gen/data/parser/validate/status'.format(id))
    parser_stopfactor_status = api_requestor.request(
        '/individual/{0}/cur_gen/data/parser/stopfactor/status'.format(id))

    parser_stopfactor_errors = api_requestor.request(
        '/individual/{0}/cur_gen/data/parser/stopfactor/errors'.format(id))

    return render(request, 'concrete/individual_scoring.html',
                  {'id': id, 'values': parser_values, 'validate': parser_validate_errors,
                   'validate_status': parser_validate_status, 'stopfactor_status': parser_stopfactor_status,
                   'stopfactors': parser_stopfactor_errors, 'sources': source_names, 'score': score});


@login_required(login_url="signin")
def source(request):
    return render(request, 'concrete/source.html')


@login_required(login_url="signin")
def reports(request):
    if request.method == 'POST':
        items = api_requestor.request('/client/{0}/'.format(request.POST['status']))
        if items == []:
            return redirect("reports");
        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        # row_headers
        for element in items[0].keys():
            worksheet.write(0, col, element)
            col += 1;
        col = 0;
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

    statuses = api_requestor.request('/client/status/')
    return render(request, 'concrete/reports.html', {'statuses': statuses})


@login_required(login_url="signin")
def individual_inspect(request, id):
    raw_data = api_requestor.request('/individual/{0}'.format(id))

    context = {
        'individual': raw_data, 'id': raw_data['id'],
        'status': raw_data['status']
    }

    return render(request, 'concrete/individual_inspect.html', context)


@login_required(login_url="signin")
def individual_operations(request, id):
    raw_data = api_requestor.request('/individual/{0}'.format(id))

    context = {
        'individual': raw_data, 'id': raw_data['id']
    }

    return render(request, 'concrete/individual_operations.html', context)


@login_required(login_url="signin")
def accept_individual(request, id):
    response = api_requestor.get("/individual/%s/ops/postscoring_accept/" % id)
    return redirect("individual_inspect", id=id);


@login_required(login_url="signin")
def reject_individual(request, id):
    response = api_requestor.get("/individual/%s/ops/postscoring_reject/" % id)
    return redirect("individual_inspect", id=id);


@login_required(login_url="signin")
def reject_individual_no_chance(request, id):
    response = api_requestor.get("/individual/%s/ops/prescoring_reject/" % id)
    return redirect("clients_list")


@login_required(login_url="signin")
def start_individual_scoring(request, id):
    response = api_requestor.get("/individual/%s/ops/scoring_start/" % id)
    return redirect("individual_inspect", id=id);


@login_required(login_url="signin")
def individual_new_generation(request, id):
    response = api_requestor.get("/individual/%s/ops/generation_next/" % id)
    return redirect("individual_inspect", id=id);


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
