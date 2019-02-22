import sys

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from rest_framework.response import Response
from portal.models import *
from portal.serializers.client_serializer import *
from portal.serializers.product_serializer import *

def get_all_clients_info():
    queryset = Client.objects.all()
    serializer = ClientGetSerializer(queryset, many=True)
    items = []
    cntr = 0
    for client in serializer.data:

        if client['product'] != 0:
            product = Product.objects.get(id=client['product'])
            field_product = product.name
        else:
            field_product = 'Not set'


        for individual in client['individuals']:
            if individual['primary'] == True:
                new_item = {}
                current_id = client['id']

                new_item['fio'] = individual['first_name'] + ' ' + individual['last_name']
                cntr += 1
                new_item['num'] = cntr
                new_item['id'] = current_id
                new_item['created_at'] = client['created_at']
                new_item['status'] = get_status(current_id)
                new_item['product'] = field_product

                items.append(new_item)
    return items


def get_current_client_info(client_id):
    queryset = Client.objects.get(id=client_id)
    client_serializer = ClientGetSerializer(queryset, many=False)
    individual = {}
    drivers = []
    for individual_raw in client_serializer.data['individuals']:
        driver = {}
        driver['name'] = individual_raw['first_name']
        driver['surname'] = individual_raw['last_name']
        driver['number'] = individual_raw['driver_license']['number']
        driver['issued_at'] = individual_raw['driver_license']['issued_at']
        driver['primary'] = individual_raw['primary']
        if individual_raw['primary'] == True:
            individual = individual_raw

        drivers.append(driver)

    items = {}
    items['id'] = client_id
    items['individual'] = individual
    items['drivers'] = drivers
    history = []

    queryset = Generation.objects.get(client_id=client_id)
    generation_serializer = GenerationSerializer(queryset, many=False)
    items['op_history'] = generation_serializer.data
    items['status'] = get_status(client_id)

    field = ''
    product_id = ''
    if client_serializer.data['product']!=0:
        product = Product.objects.get(id=client_serializer.data['product'])
        field = product.name
        product_id = product.id
    else:
        field = 'Not set'

    items['product']=field
    items['product_id'] = product_id



    return items


def new_action(data,client_id):
    serializer = NewActionSerializer(data=data)
    if serializer.is_valid():
        generation = Generation.objects.get(client_id=client_id)
        action_model = Action.objects.create(generation=generation, create_time=datetime.datetime.now(),
                                             **serializer.validated_data)
        action_serializer = ActionSerializer(action_model)
        return action_serializer.data
    return status.HTTP_400_BAD_REQUEST


def update_product(data,client_id):
    checked_data = ProductUpdateSerializer(data=data)
    if checked_data.is_valid():
        product = Product.objects.get_or_create(name=checked_data.data['product'])
        product = Product.objects.get(name=checked_data.data['product'])

        client = Client.objects.get(id=client_id)
        client.product = product.id
        client.save()
        return ClientGetSerializer(client).data


def get_status(current_id):
    queryset = Generation.objects.get(client_id=current_id)
    generation_serializer = GenerationSerializer(queryset, many=False)

    list_of_actions = generation_serializer.data['actions']

    last_action = list_of_actions[-1]['action_type']

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
    if last_action == 'scoring_checks_failed':
        return 'Ошибка на этапе пре-скоринга'
    return "Неизвестно"

# op_action = new -> Новый
# op_action = manual_decline -> Отказано до скоринга
# op_action = scoring -> Скоринг обрабатывается
# op_action = scoring_checks_failed -> Ошибка на этапе пре-скоринга
# op_action = scoring_complete_accepted -> Клиент одобрен
# op_action = scoring_complete_declined -> Клиенту отказано
