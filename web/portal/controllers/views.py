import sys
import io

from xlsxwriter.workbook import Workbook

from core.lib.constants import *

sys.path.append('../')

from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from core.lib.api import ApiRequestor


@login_required(login_url="signin")
def clients_list(request):
    items = ApiRequestor(request).get_client_all()
    statuses = ApiRequestor(request).get_client_all_status()
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses})


@login_required(login_url="signin")
def clients_list_filtered(request, status_filter):
    items = ApiRequestor(request).get_client_by_status(status_filter)
    statuses = ApiRequestor(request).get_client_all_status()
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses})


@login_required(login_url="signin")
def users_list(request):
    users = ApiRequestor(request).get_users()
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
        type = request.POST['type']
        items = []
        if type == 'general':
            items = ApiRequestor(request).get_report_basic()
        if type == 'advanced':
            items = ApiRequestor(request).get_report_advanced()
        if items == []:
            return redirect(NAME_REPORTS)
        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        # row_headers

        worksheet.write(0, 0, 'П\П №', bold)
        worksheet.write(0, 1, 'Дата заявки', bold)
        worksheet.write(0, 2, 'Дата обработки', bold)
        worksheet.write(0, 3, 'Номер заявки', bold)
        worksheet.write(0, 4, 'ФИО клиента', bold)
        worksheet.write(0, 5, 'ФИО основного клиента', bold)
        worksheet.write(0, 6, 'Статус обработки', bold)
        worksheet.write(0, 7, 'Результат проверки', bold)
        if type == 'advanced':
            worksheet.write(0, 8, 'Найдены StopFactor (список)', bold)
            worksheet.write(0, 9, 'Найдены MiddleFactor (список)', bold)
            worksheet.write(0, 10, 'Название продукта', bold)
        if type == 'general':
            worksheet.write(0, 8, 'Название продукта', bold)

        worksheet.set_column(0, 10, 10)
        worksheet.set_column(8, 9, 35)
        col = 0
        row = 1
        # row_values
        for item in items:
            wrapformat = workbook.add_format()
            wrapformat.set_text_wrap(True)
            # prepare_item = {}
            # generations = ApiRequestor(request).get_individual_info(client['primary_individual']['id'])
            # prepare_item['id'] = client['id']
            # prepare_item['date_create'] = client['created_at']
            # prepare_item['date_done'] = generations['current_generation']['actions'][1]['create_time']
            # prepare_item['willz_external_id'] = client['willz_external_id']
            # prepare_item['fio'] = client['primary_individual']['last_name']+' ' + client['primary_individual']['middle_name']+' '  + client['primary_individual']['first_name']
            # prepare_item['primary_fio'] = client['primary_individual']['last_name']+' '  + client['primary_individual']['middle_name']+' '  + client['primary_individual']['first_name']
            # prepare_item['status'] = client['primary_individual']['status']
            # stopf_status = ApiRequestor(request).get_individual_cur_data_parser_stopfactor_status(client['primary_individual']['id'])
            # validate_status = ApiRequestor(request).get_individual_cur_data_parser_validate_status(client['primary_individual']['id'])
            #
            # prepare_item['status_detailed'] = "Валидации:{0}\nСтопфакторы:{1}".format(validate_status,stopf_status)
            #
            # items_validate = ApiRequestor(request).get_individual_cur_data_parser_validate_errors(client['primary_individual']['id'])
            # prepare_item['validate_errors'] = items_validate
            # stop_list = ""
            # items_stopfactor = ApiRequestor(request).get_individual_cur_data_parser_stopfactor_errors(client['primary_individual']['id'])
            # for parser in items_stopfactor:
            #     for err in items_stopfactor[parser]:
            #         stop_list+=err['decription'] + '\n'
            # prepare_item['stopfactor_errors'] = stop_list
            # prepare_item['product']= client['product']

            for value in item:
                worksheet.write(row, col, str(item[value]), wrapformat)
                col += 1
            row += 1
            col = 0
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=" + type + ".xlsx"
        output.close()
        return response

    statuses = ApiRequestor(request).get_client_all_status()
    return render(request, URL_LINK_REPORTS, {'statuses': statuses})

