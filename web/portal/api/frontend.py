from django.contrib.sites import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg import openapi
from web.portal.serializers.frontend import *
from web.portal.serializers.backend import *
from web.portal.models import *
from django.http import Http404
from django.contrib.auth.models import User

import json
import pika

from rest_framework.renderers import JSONRenderer
from core.lib import constants
from rest_framework import viewsets
from core.lib import api_requestor


class UserListApi(mixins.ListModelMixin, mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClientsListApi(APIView):

    @swagger_auto_schema(operation_description='GET /front/clients/')
    def get(self, request):
        queryset = Client.objects.all()
        serializer = ClientGetSerializer(queryset, many=True)
        items = []
        for client in serializer.data:
             for individual in client['individuals']:
                if individual['primary'] == True:
                    new_item = {}
                    new_item['fio'] = individual['first_name'] + ' ' + individual['last_name']
                    my_id = individual['id']
                    new_item['id'] = my_id
                    new_item['created_at'] = client['created_at']

                    new_item['status'] = get_status(my_id)

                    items.append(new_item)

        return Response(items)


def get_status(individual_id):
    gen_data = api_requestor.request('/generation/{0}'.format(individual_id))
    source_cnt = 0
    check_cnt = 0
    scorint_cnt = 0
    if len(gen_data['actions'])==0:
        return 'Новая'

    for act in gen_data['actions']:
        if act['action_type'] == 'declined':
            return 'Отказано'
        if act['action_type'] == 'accepted':
            return 'Одобрено'

    return 'Неизвестен'