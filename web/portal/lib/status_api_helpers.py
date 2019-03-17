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
from portal.lib.module_api_helpers import get_generation_number

def get_dictionary_of_status():
    my_dic = {}
    my_dic['scoring_complete_declined']='Отказано'
    my_dic['scoring_complete_accepted']='Одобрено'
    my_dic['new']='Новый'
    my_dic['manual_decline']='Отказано до скоринга'
    my_dic['scoring']='Скоринг обрабатывается'
    my_dic['scoring_complete']= 'Ожидает согласования'
    my_dic['scoring_checks_failed'] = 'Техническая ошибка'
    my_dic['scoring_validate_failed'] = 'Ошибка в документах'
    my_dic['scoring_stopfactors_failed'] = 'Обнаружены стоп-факторы'
    my_dic['unknown']= 'Неизвестно'

    return my_dic


def get_status_name(status_name_internal):
    my_dic = get_dictionary_of_status()

    if status_name_internal in my_dic.keys():
        return my_dic.get(status_name_internal)
    else:
        return my_dic.get('unknown')


def get_status(individual_id):
    last_action = get_raw_status(individual_id)
    return get_status_name(last_action)


# op_action = new -> Новый
# op_action = manual_decline -> Отказано до скоринга
# op_action = scoring -> Скоринг обрабатывается
# op_action = scoring_checks_failed -> Ошибка на этапе пре-скоринга
# op_action = scoring_complete_accepted -> Клиент одобрен
# op_action = scoring_complete_declined -> Клиенту отказано



def get_raw_status(individual_id):
    queryset = Generation.objects.get(individual_id=individual_id,
                                      number=get_generation_number(individual_id,'cur_gen'))
    generation_serializer = GenerationSerializer(queryset, many=False)

    list_of_actions = generation_serializer.data['actions']

    if len(list_of_actions) != 0:
        last_action = list_of_actions[-1]['action_type']
    else:
        last_action = ''

    return last_action


def get_status_table():
    resp_status = status.HTTP_200_OK
    list_of_status = {}
    individuals = Individual.objects.all()

    if individuals.count() == 0:
        resp_status = status.HTTP_204_NO_CONTENT
    else:
        for individual in individuals:
            current_status = get_status(individual.id)
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
                if current_status == data['cur_gen']:
                    list_of_clients.append(client.id)

            if len(list_of_clients) == 0:
                resp_status = status.HTTP_204_NO_CONTENT

    return Response(status=resp_status, data=list_of_clients)


def get_list_of_states(individual_id):
    last_action = get_raw_status(individual_id)
    list_of_states = {}
    list_of_states['scoring_start'] = False
    list_of_states['prescoring_decline'] = False
    list_of_states['postscoring_reject'] = False
    list_of_states['postscoring_accept'] = False
    list_of_states['generation_next'] = False
    list_of_states['results'] = False

    if last_action == 'new':
        list_of_states['scoring_start'] = True
        list_of_states['prescoring_decline'] = True

    elif last_action == 'scoring':
        #скипаем вообще все
        return list_of_states

    elif last_action == 'scoring_complete':
        list_of_states['postscoring_reject'] = True
        list_of_states['postscoring_accept'] = True
        list_of_states['results'] = True

    elif last_action == 'scoring_complete_accepted' or last_action == 'scoring_complete_declined' \
            or last_action=='scoring_stopfactors_failed':
        list_of_states['generation_next'] = True
        list_of_states['results'] = True

    else:
        #во всех иных случаях - разрешаем новую генерацию
        list_of_states['generation_next'] = True
#            manual_decline
#            scoring_checks_failed
#            scoring_validate_failed

    return list_of_states