import sys

from portal.models import Module

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from core.lib import module_save_helper
from core.lib.modules import *
from rest_framework.response import Response
from portal.serializers.product_serializer import *
from portal.serializers.status_serializer import *


def get_status(current_id):
    last_action = get_raw_status(current_id)

    if last_action == 'scoring_complete_declined':
        return 'Отказано'
    if last_action == 'scoring_complete_accepted':
        return 'Одобрено'
    if last_action == 'new':
        return 'Новый'
    if last_action == 'manual_decline':
        return 'Отказано до скоринга'
    if last_action == 'scoring':
        return 'Скоринг обрабатывается'
    if last_action == 'scoring_complete':
        return 'Ожидает согласования'
    if last_action == 'scoring_checks_failed':
        return 'Ошибка на этапе пре-скоринга'
    return "Неизвестно"

# op_action = new -> Новый
# op_action = manual_decline -> Отказано до скоринга
# op_action = scoring -> Скоринг обрабатывается
# op_action = scoring_checks_failed -> Ошибка на этапе пре-скоринга
# op_action = scoring_complete_accepted -> Клиент одобрен
# op_action = scoring_complete_declined -> Клиенту отказано


def get_raw_status(current_id):
    queryset = Generation.objects.get(client_id=current_id)
    generation_serializer = GenerationSerializer(queryset, many=False)

    list_of_actions = generation_serializer.data['actions']

    last_action = list_of_actions[-1]['action_type']

    return last_action


def get_status_table():
    resp_status = status.HTTP_200_OK
    list_of_status = {}
    queryset = Client.objects.all()

    if queryset.count() == 0:
        resp_status = status.HTTP_204_NO_CONTENT
    else:
        for client in queryset:
            current_status = get_status(client.id)
            if current_status not in list_of_status:
                list_of_status[current_status] = 1
            else:
                list_of_status[current_status] = list_of_status[current_status]+1

    return Response(status=resp_status, data=list_of_status)


def get_clients_by_status(data):
    resp_status = status.HTTP_200_OK
    list_of_clients = []

    if 'status' not in data:
        resp_status = status.HTTP_400_BAD_REQUEST
    else:
        queryset = Client.objects.all()

        if queryset.count() == 0:
            resp_status = status.HTTP_204_NO_CONTENT
        else:
            for client in queryset:
                current_status = get_raw_status(client.id)
                if current_status == data['status']:
                    list_of_clients.append(client.id)

            if len(list_of_clients) == 0:
                resp_status = status.HTTP_204_NO_CONTENT

    return Response(status=resp_status, data=list_of_clients)

