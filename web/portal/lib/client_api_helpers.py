import sys

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from rest_framework.response import Response
from portal.models import *
from portal.serializers.client_serializer import *
from portal.serializers.product_serializer import *
from portal.lib.status_api_helpers import *
from portal.lib.product_api_helpers import get_product_name


def get_all_clients_info(filter_status=''):
    queryset = Client.objects.all()
    clients_list = []
    for client in queryset:
        client_info = get_current_client_info(client.id)

        if filter_status == '':
            clients_list.append(client_info)
        else:
            renamed_status = get_status_name(filter_status)

            if client_info['primary_individual']['status'] == renamed_status:
                clients_list.append(client_info)

    return clients_list


def get_all_clients_status():
    my_list = {}
    names_dic = get_dictionary_of_status()
    counter = 0

    for key_el in  names_dic.keys():
        element = {}
        element['name'] = names_dic.get(key_el)
        element['count'] = 0
        my_list[key_el] = element

    queryset = Client.objects.all()

    for client in queryset:
        client_info = get_current_client_info(client.id)
        status_name = client_info['primary_individual']['status']
        counter += 1

        key_in_list = False
        for key_el in names_dic.keys():
            if names_dic.get(key_el) == status_name:
                my_list[key_el]['count'] += 1
                key_in_list = True
                break

        if key_in_list == False:
            my_list['unknown']['count'] += 1

    final_list = {}
    if my_list.get('unknown'): my_list.pop('unknown')
    final_list['total'] = counter
    final_list['data'] = my_list
    return final_list


def get_current_client_info(client_id):
    queryset = Client.objects.get(id=client_id)
    client_serializer = ClientGetSerializer(queryset, many=False)

    primary_individual = {}
    secondary_individuals = []
    individuals_count = 0

    for individual_raw in client_serializer.data['individuals']:
        individuals_count += 1
        individual = Individual.objects.get(id=individual_raw['id'])
        individual_serializer = IndividualGetSerializer(individual, many=False)
        status = get_status(individual_raw['id'])

        if individual_raw['primary'] == True:
            primary_individual = individual_serializer.data
            primary_individual['status'] = status
            primary_individual['status_buttons'] = get_list_of_states(individual_raw['id'])
        else:
            secondary_individual = individual_serializer.data
            secondary_individual['status'] = status
            secondary_individual['status_buttons'] = get_list_of_states(individual_raw['id'])

            secondary_individuals.append(secondary_individual)

    client_view_serializer = ClientViewSerializer(queryset, many=False)

    response_data = {}
    response_data = client_view_serializer.data
    response_data['product'] = get_product_name(queryset.product)
    response_data['individuals_count'] = individuals_count
    response_data['primary_individual'] = primary_individual
    response_data['secondary_individuals'] = secondary_individuals

    return response_data


def new_action(data, individual_id, generation_number):
    serializer = NewActionSerializer(data=data)
    if serializer.is_valid():
        generation = Generation.objects.get(individual_id=individual_id, number=generation_number)
        action_model = Action.objects.create(generation=generation, create_time=datetime.datetime.now(),
                                             **serializer.validated_data)
        action_serializer = ActionSerializer(action_model)
        return Response(status=status.HTTP_201_CREATED, data=action_serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def update_product(data, client_id):
    checked_data = ProductUpdateSerializer(data=data)
    if checked_data.is_valid():
        product = Product.objects.get_or_create(name=checked_data.data['product'])
        product = Product.objects.get(name=checked_data.data['product'])

        client = Client.objects.get(id=client_id)
        client.product = product.id
        client.save()
        client_serializer = ClientGetSerializer(client)
        return Response(status=status.HTTP_202_ACCEPTED, data=client_serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def post_client(data):
    client_serializer = ClientSerializer(data=data)
    if client_serializer.is_valid():
        client_serializer.save()
        return Response(data=client_serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def post_existing_client(data,id):
    client_serializer = ClientSerializer(data=data)
    if client_serializer.is_valid():

        queryset = Client.objects.filter(id=id)
        validated_data = client_serializer.validated_data
        individuals_data = validated_data.pop('individuals')
        client = queryset.update(**validated_data)


        for individual_data in individuals_data:
            passport_data = individual_data.pop('passport')
            driver_license_data = individual_data.pop('driver_license')

            queryset = Individual.objects.filter(client=client)
            individual = queryset.update(**individual_data)
            #Generation.objects.create(individual=individual, number=1, create_time=datetime.datetime.now(),
             #                         is_archive=False)

            passport_images_data = passport_data.pop('images')
            queryset = Passport.objects.filter(individual=individual)
            passport = queryset.update(**passport_data)

            for passport_image_data in passport_images_data:
                queryset = PassportImage.objects.filter(passport=passport)
                queryset.update(**passport_image_data)

            driver_license_images_data = driver_license_data.pop('images')
            queryset = DriverLicense.objects.filter(individual=individual)
            driver_license = queryset.update(**driver_license_data)

            for driver_license_image_data in driver_license_images_data:
                queryset = DriverLicenseImage.objects.filter(driver_license=driver_license)
                queryset.update(**driver_license_image_data)

        queryset = Client.objects.get(id=id)
        cur_client = ClientSerializer(queryset)
        return Response(data=cur_client.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


