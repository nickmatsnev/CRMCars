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
        items = ApiRequestor(request).get_client_by_status(request.POST['status'])
        if items == []:
            return redirect(NAME_REPORTS)
        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        # row_headers
        for element in items[0].keys():
            worksheet.write(0, col, element)
            col += 1
        col = 0
        row = 1
        # row_values
        for client in items:
            prepare_item = {}
            prepare_item['id'] = client['id']
            prepare_item['date_create'] = client['created_at']

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

    statuses = ApiRequestor(request).get_client_all_status()
    return render(request, URL_LINK_REPORTS, {'statuses': statuses})

