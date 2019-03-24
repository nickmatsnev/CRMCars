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
from portal.lib.api_requestor import *
from portal.models import Module
from rest_framework import status
from portal.lib.constants import *


@login_required(login_url="signin")
def individual_scoring(request, id):
    #   res = get_scorista()

    individual_id = get_individual_info(id)
    sources_done = get_individual_cur_data_info(id,URL_MODULE_SOURCE)
    source_names = []
    for item in sources_done:
        source_names.append(item)
    score = get_individual_cur_data_info(id, URL_MODULE_SCORING, URL_INDIVIDUAL_METHOD_SCORE)
    # scoring_data = api_requestor.request('/individual/{0}/cur_gen/data/{1}/'.format(id, "scoring"))
    parser_values = get_individual_cur_data_info(id, URL_MODULE_PARSER, URL_INDIVIDUAL_METHOD_VALUES)
    parser_validate_errors = get_individual_cur_data_info(id, URL_MODULE_PARSER, URL_INDIVIDUAL_METHOD_VALIDATE_ERRORS)
    parser_validate_status = get_individual_cur_data_info(id, URL_MODULE_PARSER, URL_INDIVIDUAL_METHOD_VALIDATE_STATUS)
    parser_stopfactor_status = get_individual_cur_data_info(id, URL_MODULE_PARSER, URL_INDIVIDUAL_METHOD_STOP_STATUS)

    parser_parameters = get_module_info(URL_MODULE_PARSER,URL_MODULE_METHOD_VIEW_PARAMETERS)
    parameters_dict = {}
    for item in parser_parameters:
        parameters_dict[item['name']] = item['description']

    parser_stopfactor_errors = get_individual_cur_data_info(id, URL_MODULE_PARSER, URL_INDIVIDUAL_METHOD_STOP_ERRORS)

    return render(request, URL_LINK_INDIVIDUAL_SCORING,
                  {'id': id, 'values': parser_values, 'validate': parser_validate_errors,
                   'validate_status': parser_validate_status, 'stopfactor_status': parser_stopfactor_status,
                   'stopfactors': parser_stopfactor_errors, 'sources': source_names, 'score': score,
                   'parameters_dict': parameters_dict})


@login_required(login_url="signin")
def individual_prescoring_decline(request, id):
    raw_data = get_client_info(id,URL_CLIENT_METHOD_VIEW)

    context = {'individual': raw_data['individual'], 'id': raw_data['id'], 'drivers': raw_data['drivers'],
               'history': raw_data['op_history']}

    return render(request, URL_LINK_CLIENT_DECLINE, context)


@login_required(login_url="signin")
def individual_inspect(request, id):
    raw_data = get_individual_info(id)

    context = {
        'individual': raw_data, 'id': raw_data['id'],
        'status': raw_data['status']
    }

    return render(request, URL_LINK_INDIVIDUAL_INSPECT, context)


@login_required(login_url="signin")
def individual_operations(request, id):
    raw_data = get_individual_info(id)

    context = {
        'individual': raw_data, 'id': raw_data['id']
    }

    return render(request, URL_LINK_INDIVIDUAL_OPERATIONS, context)


@login_required(login_url="signin")
def accept_individual(request, id):
    respone = do_individual_ops(id,URL_INDIVIDUAL_OPS_POST_ACCEPT)
    sleep(0.9)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def reject_individual(request, id):
    respone = do_individual_ops(id, URL_INDIVIDUAL_OPS_POST_REJECT)
    sleep(0.9)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def reject_individual_no_chance(request, id):
    respone = do_individual_ops(id, URL_INDIVIDUAL_OPS_PRE_REJECT)
    sleep(0.5)
    return redirect(URL_CLIENTS_LIST)


@login_required(login_url="signin")
def start_individual_scoring(request, id):
    respone = do_individual_ops(id, URL_INDIVIDUAL_OPS_START)
    sleep(0.5)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def individual_new_generation(request, id):
    respone = do_individual_ops(id, URL_INDIVIDUAL_OPS_GEN_NEXT)
    sleep(0.5)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)
