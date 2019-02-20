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


def set_module_name(where,name):
    module_id = where[name]

    if module_id != 0:
        queryset = Module.objects.get(id=module_id)
        return queryset.name
    else:
        return "Not selected"

