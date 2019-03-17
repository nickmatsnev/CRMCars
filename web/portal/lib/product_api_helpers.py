import sys

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from rest_framework.response import Response
from portal.models import *
from portal.serializers.product_serializer import *
from portal.lib.module_api_helpers import view_module_by_type

from portal.lib.json_helpers import  *


def get_all_products_info():
    queryset = Product.objects.all()
    serializer = ProductGetSerializer(queryset, many=True)
    items = []

    for item in serializer.data:
            new_item = {}
            new_item['id'] = item['id']
            new_item['name'] = item['name']
            new_item['primary'] = set_module_name(item,"primary_scoring")
            new_item['other'] = set_module_name(item, "other_scoring")
            items.append(new_item)

    return items


def get_product_name(product_id):
    queryset = Product.objects.get(id=product_id)
    return queryset.name


def get_product_id_for_individual(individual_id):
    module_id = 0
    individual = Individual.objects.filter(id=individual_id)
    if individual.count()!=0:
        individual = Individual.objects.get(id=individual_id)
        client = individual.client
        product = Product.objects.get(id=client.product)

        if individual.primary == True:
            module_id = product.primary_scoring
        else:
            module_id = product.other_scoring
    return module_id


def set_module_name(where,name):
    module_id = where[name]

    if module_id != 0:
        queryset = Module.objects.get(id=module_id)
        return queryset.name
    else:
        return "Not selected"

