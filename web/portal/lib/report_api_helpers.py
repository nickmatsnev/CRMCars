import sys

from portal.models import Module

sys.path.append('../../')
sys.path.append('..')

from core.lib.api import ApiRequestor
from portal.lib.status_api_helpers import *


def get_base_report(request):
    json_response = []
    all_clients = ApiRequestor(request).get_client_all()

    for client in all_clients:
        individuals_json = []
        individuals_json.append(client['primary_individual'])
        for individ in client['secondary_individuals']:
            individuals_json.append(individ)

        for individ in individuals_json:
            json_item = {}
            json_item['id'] = individ['id']
            json_item["request_date"] = client["created_at"]

            report_info = get_report_info(individ["id"])
            json_item["complete_date"] = report_info["complete_date"]
            json_item["request_number"] = client["willz_external_id"]
            json_item["fio_client"] = individ["last_name"] + ' ' + \
                                      individ["first_name"] + ' ' + \
                                      individ["middle_name"] + ' '
            json_item["fio_primary_individual"] = client["primary_individual"]["last_name"] + ' ' + \
                                                  client["primary_individual"]["first_name"] + ' ' + \
                                                  client["primary_individual"]["middle_name"] + ' '
            json_item["processing_status"] = report_info["processing_status"]
            json_item["check_status"] = report_info["check_status"]
            # json_item["company_name"] = "???"
            json_item["product_name"] = client["product"]
            # json_item["fio_operator"] = "???"
            json_response.append(json_item)

    return json_response


def get_advanced_report(request):
    json_response = []
    all_clients = ApiRequestor(request).get_client_all()

    for client in all_clients:
        individuals_json = []
        individuals_json.append(client['primary_individual'])
        for individ in client['secondary_individuals']:
            individuals_json.append(individ)

        for individ in individuals_json:
            json_item = {}
            json_item['id'] = individ['id']
            json_item["request_date"] = client["created_at"]

            report_info = get_report_info(individ["id"])
            json_item["complete_date"] = report_info["complete_date"]
            json_item["request_number"] = client["willz_external_id"]
            json_item["fio_client"] = individ["last_name"] + ' ' + \
                                      individ["first_name"] + ' ' + \
                                      individ["middle_name"] + ' '
            json_item["fio_primary_individual"] = client["primary_individual"]["last_name"] + ' ' + \
                                                  client["primary_individual"]["first_name"] + ' ' + \
                                                  client["primary_individual"]["middle_name"] + ' '
            json_item["processing_status"] = report_info["processing_status"]
            json_item["check_status"] = report_info["check_status"]
            stopf = ""
            validate = ""
            if report_info["check_status"] == "Одобрено" or report_info["check_status"] == "Отказано":
                validate = ApiRequestor(request).get_individual_cur_data_parser_validate_errors(
                    client['primary_individual']['id'])
                stopfactors = ApiRequestor(request).get_individual_cur_data_parser_stopfactor_errors(
                    client['primary_individual']['id'])
                for module in stopfactors:
                    for factor in stopfactors[module]:
                        stopf += "Найден стопфактор: " + factor['decription'] + "\n"
                if validate == {}:
                    validate = "Не найдено"
                if stopf == {}:
                    stopf = "Не найдено"
            json_item['stop_factors'] = validate
            json_item['middle_factors'] = stopf
            # json_item["company_name"] = "???"
            json_item["product_name"] = client["product"]
            # json_item["fio_operator"] = "???"
            json_response.append(json_item)

    return json_response