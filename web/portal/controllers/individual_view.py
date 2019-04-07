import sys
from time import sleep

sys.path.append('../')

from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from portal.lib.api_requestor import *
from core.lib.constants import *


@login_required(login_url="signin")
def individual_scoring(request, id):
    #   res = get_scorista()

    individual_id = get_individual_info(id)
    sources_done = get_individual_cur_data_source(id)
    source_names = []
    for item in sources_done:
        source_names.append(item)
    score = get_individual_cur_data_score(id)
    # scoring_data = api_requestor.request('/individual/{0}/cur_gen/data/{1}/'.format(id, "scoring"))
    parser_values = get_individual_cur_data_parser_values(id)
    parser_validate_errors = get_individual_cur_data_parser_validate_errors(id)
    parser_validate_status = get_individual_cur_data_parser_validate_status(id)
    parser_stopfactor_status = get_individual_cur_data_parser_stopfactor_status(id)

    parser_parameters = get_module_parser_parameters()
    parameters_dict = {}
    for item in parser_parameters:
        parameters_dict[item['name']] = item['description']

    parser_stopfactor_errors = get_individual_cur_data_parser_stopfactor_errors(id)

    return render(request, URL_LINK_INDIVIDUAL_SCORING,
                  {'id': id, 'values': parser_values, 'validate': parser_validate_errors,
                   'validate_status': parser_validate_status, 'stopfactor_status': parser_stopfactor_status,
                   'stopfactors': parser_stopfactor_errors, 'sources': source_names, 'score': score,
                   'parameters_dict': parameters_dict})


@login_required(login_url="signin")
def individual_prescoring_decline(request, id):
    raw_data = get_client_view(id)

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
    response = do_individual_accept(id)
    sleep(0.9)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def reject_individual(request, id):
    response = do_individual_reject(id)
    sleep(0.9)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def reject_individual_no_chance(request, id):
    response = do_individual_pre_reject(id)
    sleep(0.5)
    return redirect(URL_CLIENTS_LIST)


@login_required(login_url="signin")
def start_individual_scoring(request, id):
    response = do_individual_start(id)
    sleep(0.5)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def individual_new_generation(request, id):
    response = do_individual_next(id)
    sleep(0.5)
    return redirect(URL_INDIVIDUAL_INSPECT, id=id)
