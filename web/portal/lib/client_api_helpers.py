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

    items['product'] = client_serializer.data['product']

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

        product = Product.objects.filter(name=checked_data.data['product'])
        if product is None:
            product = Product.objects.create(name=checked_data.data['product'])
            product.save()

        product = Product.objects.get(name=checked_data.data['product'])

        serializer = ProductSerializer(product)
# TODO: Тут какая-то хрень с обновлением продукта - пока не понял как many-to-many обновить можно
        client = Client.objects.get(id=client_id)
        client.product.clear()
        client.product.add(serializer)
        client.save()

        client_serializer = ClientGetSerializer(client)
        return client_serializer.data


def get_status(current_id):
    queryset = Generation.objects.get(client_id=current_id)
    generation_serializer = GenerationSerializer(queryset, many=False)

    source_cnt = 0
    check_cnt = 0
    scorint_cnt = 0
    declined = False
    accepted = False
    new = False

    for act in generation_serializer.data['actions']:
        if act['action_type'] == 'declined':
            declined =  True
        if act['action_type'] == 'accepted':
            accepted = True
        if act['action_type'] == 'new':
            new = True

    # определить что выше по приоритетам!
    if declined==True:
        return 'Отказано'
    if accepted==True:
        return 'Одобрено'
    if new==True:
        return 'Новый'

    return 'Неизвестно'