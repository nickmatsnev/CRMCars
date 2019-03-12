import sys

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from rest_framework.response import Response
from portal.models import *
from portal.serializers.client_serializer import *
from portal.serializers.product_serializer import *
from portal.lib.status_api_helpers import get_status


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
                current_id = individual['id']

                new_item['fio'] = individual['first_name'] + ' ' + individual['last_name']
                cntr += 1
                new_item['num'] = cntr
                new_item['id'] = individual['id']
                new_item['willz_external_id'] = individual['willz_external_id']
                new_item['created_at'] = client['created_at']
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

#    queryset = Generation.objects.get(client_id=client_id)
#    generation_serializer = GenerationSerializer(queryset, many=False)
 #   items['op_history'] = generation_serializer.data
#    items['status'] = get_status(client_id)

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


def new_action(data,individual_id, generation_number):
    serializer = NewActionSerializer(data=data)
    if serializer.is_valid():
        generation = Generation.objects.get(individual_id=individual_id,number=generation_number)
        action_model = Action.objects.create(generation=generation, create_time=datetime.datetime.now(),
                                             **serializer.validated_data)
        action_serializer = ActionSerializer(action_model)
        return Response(status=status.HTTP_201_CREATED,data=action_serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def update_product(data,client_id):
    checked_data = ProductUpdateSerializer(data=data)
    if checked_data.is_valid():
        product = Product.objects.get_or_create(name=checked_data.data['product'])
        product = Product.objects.get(name=checked_data.data['product'])

        client = Client.objects.get(id=client_id)
        client.product = product.id
        client.save()
        client_serializer = ClientGetSerializer(client)
        return Response(status=status.HTTP_202_ACCEPTED,data=client_serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

