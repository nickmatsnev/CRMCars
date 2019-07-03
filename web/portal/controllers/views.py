import sys
import io
import json
from xlsxwriter.workbook import Workbook
from datetime import datetime

from core.lib.constants import *
from core.lib import constants
from core.lib import log_reader
from core.lib.image_worker import save_photo

sys.path.append('../')

from portal.controllers.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from core.lib.api import ApiRequestor
from web.portal.lib.client_forms import SearchForm
from web.portal.templatetags import gender_filter
from core.lib.datetime_converters import date_converter

@login_required(login_url="signin")
def clients_list(request):
    # myCommand* = (void*)*ApiRequestor(request).get_client_all()
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
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses, 'form': form})


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
    return render(request, URL_LINK_CLIENTS_LIST, {'items': items, 'statuses': statuses, 'form': form})


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

        # formats
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
                worksheet.write(row, col, str(item[value]), wrap_or_not_wrap)
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
                                                  "logs_scoring": logs_scoring, "logs_sources": logs_sources})


@login_required(login_url="signin")
def upload_client_manually(request):
    if request.method == 'POST':
        form = UploadClientForm(request.POST)

        if len(request.FILES) != 0:
            for x in range(1, 5):
                if f'passport_image_{x}' in request.FILES:
                    path = save_photo(request.FILES[f'passport_image_{x}'], request.user.id)
                    form.initial[f'passport_image_{x}_url'] = path

            for y in range(1, 3):
                if f'driver_license_image_{y}' in request.FILES:
                    path = save_photo(request.FILES[f'driver_license_image_{y}'], request.user.id)
                    form.initial[f'driver_license_image_{y}_url'] = path

        else:
            if form.is_valid():
                cd = form.cleaned_data
                new_client = {}
                new_client['willz_external_id'] = 0
                new_client['created_at'] = datetime.now().__str__()
                individuals = []

                individual = {}
                individual['willz_external_id'] = 0
                individual['primary'] = True
                individual['last_name'] = cd['last_name']
                individual['first_name'] = cd['first_name']
                individual['middle_name'] = cd['middle_name']
                individual['email'] = cd['email']
                individual['phone'] = cd['phone']
                individual['gender'] = gender_filter.gender_back_filter(cd['gender'])
                individual['birthday'] = cd['birthday'].__str__()

                passport = {}
                passport['number'] = cd['passport_number']
                passport['issued_at'] = cd['passport_issued_at'].__str__()
                passport['issued_by'] = cd['passport_issued_by']
                passport['address_registration'] = cd['passport_address_registration']
                passport['division_code'] = cd['passport_division_code']
                passport['birthplace'] = cd['passport_birthplace']

                pass_images = []
                for x in range(1,5):
                    image = {}
                    image['title'] = 'manual'
                    image['url'] = cd[f'passport_image_{x}_url']
                    pass_images.append(image)

                passport['images'] = pass_images
                individual['passport'] = passport

                license = {}
                license['number'] = cd['driver_license_number']
                license['issued_at'] = cd['driver_license_issued_at'].__str__()

                license_images = []
                for x in range(1, 3):
                    image = {}
                    image['title'] = 'manual'
                    image['url'] = cd[f'driver_license_image_{x}_url']
                    license_images.append(image)

                license['images'] = license_images
                individual['driver_license'] = license

                individuals.append(individual)
                new_client['individuals'] = individuals

                json_data = json.dumps(new_client)
                client = ApiRequestor(request).get_client_from_raw_willz(json_data)

                client_id = client['id']

                json_data = json.dumps({"product": "Willz"})
                response = ApiRequestor(request).update_client_product(client_id, json_data)

                for individual in client['individuals']:
                    ApiRequestor(request).add_action(individual['id'], NAME_NEW, request.user.username,
                                                  payload=CLIENT_PROCESSOR_MANUAL_SUCCESS)
                #TODO: Куда редирект делаем???
                return redirect('/'+NAME_CLIENTS_LIST +NAME_HTML)

            return HttpResponse(f'Error {form.errors}')

    else:
        form = UploadClientForm()
    return render(request, "concrete/forms/upload_client.html", {'form': form})
