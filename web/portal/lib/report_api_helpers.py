import sys

from portal.models import Module

sys.path.append('../../')
sys.path.append('..')

from core.lib.api import ApiRequestor
from portal.lib.status_api_helpers import *
from core.lib.global_settings import *

from xlsxwriter.workbook import Workbook

def _check_text_width(header_element,text):
    text_width = len(text)+1

    if text_width>header_element['width']:
        if text_width>EXCEL_COLUMN_WIDTH_MAX:
            header_element['width'] = EXCEL_COLUMN_WIDTH_MAX
            header_element['wrap'] = True
        else:
            header_element['width'] = text_width


def _append_fio(json_array):
    return json_array["last_name"] + ' ' + \
            json_array["first_name"] + ' ' + \
            json_array["middle_name"] + ' '


def _get_column_for_header(column_number,name, bold):
    header_element = {}
    header_element['col'] = column_number
    header_element['text'] = name
    header_element['bold'] = bold
    col_width = len(name)+1
    header_element['width'] = col_width if col_width > EXCEL_COLUMN_WIDTH_BASE else EXCEL_COLUMN_WIDTH_BASE
    header_element['wrap'] = False
    return header_element


def _get_all_columns_for_header(advanced=False):
    json_header = []

    json_header.append(_get_column_for_header(0, 'П\П №',True))
    json_header.append(_get_column_for_header(1, 'Дата заявки', True))
    json_header.append(_get_column_for_header(2, 'Дата обработки', True))
    json_header.append(_get_column_for_header(3, 'Номер заявки', True))
    json_header.append(_get_column_for_header(4, 'ФИО клиента', True))
    json_header.append(_get_column_for_header(5, 'ФИО основного клиента', True))
    json_header.append(_get_column_for_header(6, 'Статус обработки', True))
    json_header.append(_get_column_for_header(7, 'Результат проверки', True))

    if advanced==True:
        json_header.append(_get_column_for_header(8, 'Найдены StopFactor (список)', True))
        json_header.append(_get_column_for_header(9, 'Найдены MiddleFactor (список)', True))
        json_header.append(_get_column_for_header(10, 'Название продукта', True))
    else:
        json_header.append(_get_column_for_header(8, 'Название продукта', True))

    return json_header


def get_standard_report(request,advanced=False):
    json_response = {}

    json_response['headers'] = _get_all_columns_for_header(advanced)

    report_data = []

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
            _check_text_width(json_response['headers'][1], json_item["request_date"])
            report_info = get_report_info(individ["id"])
            json_item["complete_date"] = report_info["complete_date"]
            _check_text_width(json_response['headers'][2], json_item["complete_date"])
            json_item["request_number"] = client["willz_external_id"]
            json_item["fio_client"] = _append_fio(individ)
            _check_text_width(json_response['headers'][4], json_item["fio_client"])
            json_item["fio_primary_individual"] = _append_fio(client["primary_individual"])
            _check_text_width(json_response['headers'][5], json_item["fio_primary_individual"])
            json_item["processing_status"] = report_info["processing_status"]
            _check_text_width(json_response['headers'][6], json_item["processing_status"])
            json_item["check_status"] = report_info["check_status"]
            json_item["product_name"] = client["product"]

            if advanced==True:
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
                _check_text_width(json_response['headers'][8], json_item["stop_factors"])
                json_item['middle_factors'] = stopf
                _check_text_width(json_response['headers'][9], json_item["middle_factors"])

            report_data.append(json_item)

    json_response['data'] = report_data

    return json_response

