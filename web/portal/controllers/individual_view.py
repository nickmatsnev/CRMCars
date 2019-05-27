import sys
from time import sleep

from core.lib import parser_values_converter

sys.path.append('../')

from django.contrib.auth.decorators import login_required
from django.shortcuts import *

from core.lib.constants import *
from core.lib.api import ApiRequestor


@login_required(login_url="signin")
def individual_scoring(request, id, gen_id_or_cur_gen):
    #   res = get_scorista()
    apiRequestor = ApiRequestor(request)
    individual = apiRequestor.get_individual_info(id)
    sources_done = apiRequestor.get_individual_data_source(id, gen=gen_id_or_cur_gen)
    source_names = []
    for item in sources_done:
        source_names.append(item)
    score = format(apiRequestor.get_individual_data_score(id, gen=gen_id_or_cur_gen), '.0f')
    # scoring_data = api_requestor.request('/individual/{0}/cur_gen/data/{1}/'.format(id, "scoring"))
    parser_values = apiRequestor.get_individual_data_parser_values(id, gen=gen_id_or_cur_gen)
    parser_validate_errors = apiRequestor.get_individual_data_parser_validate_errors(id, gen=gen_id_or_cur_gen)
    parser_validate_status = apiRequestor.get_individual_data_parser_validate_status(id, gen=gen_id_or_cur_gen)
    parser_stopfactor_status = apiRequestor.get_individual_data_parser_stopfactor_status(id, gen=gen_id_or_cur_gen)

    parser_parameters = apiRequestor.get_module_parser_parameters()
    parameters_dict = {}
    for item in parser_parameters:
        parameters_dict[item['name']] = item['description']

    parser_stopfactor_errors = apiRequestor.get_individual_data_parser_stopfactor_errors(id, gen=gen_id_or_cur_gen)

    return render(request, URL_LINK_INDIVIDUAL_SCORING,
                  {'id': id, 'values': parser_values, 'validate': parser_validate_errors,
                   'validate_status': parser_validate_status, 'stopfactor_status': parser_stopfactor_status,
                   'stopfactors': parser_stopfactor_errors, 'sources': source_names, 'score': score,
                   'parameters_dict': parameters_dict, 'individual': individual})


@login_required(login_url="signin")
def individual_report(request, id, gen_id_or_cur_gen):
    #   res = get_scorista()
    apiRequestor = ApiRequestor(request)
    individual = apiRequestor.get_individual_info(id)
    sources_done = apiRequestor.get_individual_data_source(id, gen=gen_id_or_cur_gen)
    source_names = []
    for item in sources_done:
        source_names.append(item)
    score = apiRequestor.get_individual_data_score(id, gen=gen_id_or_cur_gen)
    # scoring_data = api_requestor.request('/individual/{0}/cur_gen/data/{1}/'.format(id, "scoring"))
    parser_values = apiRequestor.get_individual_data_parser_values(id, gen=gen_id_or_cur_gen)
    parser_values_dictionary = parser_values_converter.get_parser_values(parser_values)
    parser_validate_errors = apiRequestor.get_individual_data_parser_validate_errors(id, gen=gen_id_or_cur_gen)
    parser_validate_status = apiRequestor.get_individual_data_parser_validate_status(id, gen=gen_id_or_cur_gen)
    parser_stopfactor_status = apiRequestor.get_individual_data_parser_stopfactor_status(id, gen=gen_id_or_cur_gen)

    parser_parameters = apiRequestor.get_module_parser_parameters()
    parameters_dict = {}
    for item in parser_parameters:
        parameters_dict[item['name']] = item['description']

    parser_stopfactor_errors = apiRequestor.get_individual_data_parser_stopfactor_errors(id, gen=gen_id_or_cur_gen)

    return render(request, URL_LINK_INDIVIDUAL_REPORT,
                  {'id': id, 'parser_values': parser_values_dictionary, 'validate': parser_validate_errors,
                   'validate_status': parser_validate_status, 'stopfactor_status': parser_stopfactor_status,
                   'stopfactors': parser_stopfactor_errors, 'sources': source_names, 'score': score,
                   'individual': individual,
                   'parameters_dict': parameters_dict})

@login_required(login_url="signin")
def individual_prescoring_decline(request, id):
    raw_data = ApiRequestor(request).get_client_view(id)

    context = {'individual': raw_data['individual'], 'id': raw_data['id'], 'drivers': raw_data['drivers'],
               'history': raw_data['op_history']}

    return render(request, URL_LINK_CLIENT_DECLINE, context)


@login_required(login_url="signin")
def individual_inspect(request, id):
    raw_data = ApiRequestor(request).get_individual_info(id)

    context = {
        'individual': raw_data, 'id': raw_data['id'],
        'status': raw_data['status']
    }

    return render(request, URL_LINK_INDIVIDUAL_INSPECT, context)


@login_required(login_url="signin")
def individual_operations(request, id, gen_id_or_cur_gen):
    raw_data = ApiRequestor(request).get_individual_info(id)

    context = {
        'individual': raw_data, 'id': raw_data['id']
    }

    return render(request, URL_LINK_INDIVIDUAL_OPERATIONS, context)


@login_required(login_url="signin")
def accept_individual(request, id):
    response = ApiRequestor(request).do_individual_accept(id)
    sleep(0.9)
    return redirect(NAME_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def reject_individual(request, id):
    response = ApiRequestor(request).do_individual_reject(id)
    sleep(0.9)
    return redirect(NAME_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def reject_individual_no_chance(request, id):
    response = ApiRequestor(request).do_individual_pre_reject(id)
    sleep(0.5)
    return redirect(NAME_CLIENTS_LIST)


@login_required(login_url="signin")
def start_individual_scoring(request, id):
    response = ApiRequestor(request).do_individual_start(id)
    sleep(0.5)
    return redirect(NAME_INDIVIDUAL_INSPECT, id=id)


@login_required(login_url="signin")
def individual_new_generation(request, id):
    response = ApiRequestor(request).do_individual_next(id)
    sleep(0.5)
    return redirect(NAME_INDIVIDUAL_INSPECT, id=id)
