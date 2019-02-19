import sys

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from rest_framework.response import Response
from portal.models import *
from portal.serializers.product_serializer import *


def get_all_products_info():
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    items = []

    for item in serializer.data:
        new_item = {}

        new_item['product'] = item['name']
        new_item['primary'] = build_sub_table(item['primary_scoring'])
        new_item['other'] = build_sub_table(item['other_scoring'])

        items.append(new_item)
    return items


def build_sub_table(where):
    table = {}
    table['type'] = check_for_field(where,'type')
    table['name'] = check_for_field(where,'name')
    table['is_active'] = check_for_field(where,'is_active')
    return table



def check_for_field(where,what):
    if where is not None:
        if where[what] is not None:
            return where[what]
        else:
            return ""
    else:
        return ""