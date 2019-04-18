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
        json_item = {}
        json_item["request_date"] = client["created_at"]

        report_info = get_report_info(client["primary_individual"]["id"])
        json_item["complete_date"] = report_info["complete_date"]
        json_item["request_number"] = client["id"]
        json_item["fio_client"] = client["primary_individual"]["last_name"] + ' ' + \
                                  client["primary_individual"]["first_name"] + ' ' + \
                                  client["primary_individual"]["middle_name"] + ' '
        json_item["fio_primary_individual"] = client["primary_individual"]["last_name"] + ' ' + \
                                              client["primary_individual"]["first_name"] + ' ' + \
                                              client["primary_individual"]["middle_name"] + ' '
        json_item["processing_status"] = report_info["processing_status"]
        json_item["check_status"] = report_info["check_status"]
        json_item["company_name"] = "???"
        json_item["product_name"] = client["product"]
        json_item["fio_operator"] = "???"
        json_response.append(json_item)

    return json_response

