import sys
import io
import json
from xlsxwriter.workbook import Workbook

from core.lib.constants import *
from core.lib import constants
from core.lib import log_reader
sys.path.append('../')


from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from core.lib.api import ApiRequestor
from web.portal.lib.client_forms import SearchForm


@login_required(login_url="signin")
def clients_list(request):
    #myCommand* = (void*)*ApiRequestor(request).get_client_all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            items = ApiRequestor(request).get_client_by_status_or_surname(cd['surnameSearch'])
        else:
            items = ApiRequestor(request).get_client_all()
    else:
        items = ApiRequestor(request).get_client_all()

    statuses = ApiRequestor(request).get_client_all_status()
    form = SearchForm()
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses, 'form':form})


@login_required(login_url="signin")
def clients_list_filtered(request, status_filter):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            items = ApiRequestor(request).get_client_by_status_or_surname(cd['surnameSearch'])
        else:
            items = ApiRequestor(request).get_client_by_status_or_surname(status_filter)
    else:
        items = ApiRequestor(request).get_client_by_status_or_surname(status_filter)
    statuses = ApiRequestor(request).get_client_all_status()
    form = SearchForm()
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses, 'form':form})


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
        resp = {}
        if type == NAME_GENERAL:
            resp = ApiRequestor(request).get_report_basic()
        if type == NAME_ADVANCED:
            resp = ApiRequestor(request).get_report_advanced()
        if resp['data'] == {}:
            return redirect(NAME_REPORTS)

        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        #formats
        bold = workbook.add_format({'bold': True})
        not_bold = workbook.add_format({'bold': False})
        wrap = workbook.add_format({'text_wrap': True})
        not_wrap = workbook.add_format({'text_wrap': False})

        # row_headers
        for new_column in resp['headers']:
            worksheet.set_column(new_column['col'], new_column['col'], new_column['width'])
            bold_or_not_bold = not_bold if new_column['col'] is False else bold
            worksheet.write(0, new_column['col'], new_column['text'], bold_or_not_bold)

        # row_values
        col = 0
        row = 1
        for item in resp['data']:
            for value in item:
                wrap_or_not_wrap = not_wrap if resp['headers'][col]['wrap'] is False else wrap
                worksheet.write(row, col, str(item[value]),wrap_or_not_wrap)
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


@login_required(login_url="signin")
def worker_logs(request):
    logs_client = log_reader.read_log(constants.CLIENT_PROCESSOR_NAME)
    logs_sources = log_reader.read_log(constants.SOURCE_PROCESSOR_NAME)
    logs_parser = log_reader.read_log(constants.PARSER_PROCESSOR_NAME)
    logs_scoring = log_reader.read_log(constants.SCORING_PROCESSOR_NAME)

    return render(request, "concrete/logs.html", {"logs_client": logs_client, "logs_parser": logs_parser,
                                                  "logs_scoring": logs_scoring, "logs_sources": logs_sources});
