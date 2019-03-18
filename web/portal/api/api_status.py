import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender, api_requestor
from portal.lib.status_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.models import *
from core.lib import action_helper
from portal.lib.product_api_helpers import get_product_id_for_individual
from django.contrib.auth.models import User


class MainApi(APIView):
    @swagger_auto_schema(operation_description='Get table of statuses', responses={200: StatusSerializer,
                                                                                   204: 'No content'})
    def get(self, request,):
        return get_status_table()

    @swagger_auto_schema(operation_description='Get clients for current status', request_body=GetStatusSerializer,
                            responses={200: GetStatusSerializer,
                                       400: 'No field status in request',
                                       204: 'No clients with current status'
                                       })
    def post(self, request):
        return get_clients_by_status(request.data)


class PostReject(APIView):
        @swagger_auto_schema(operation_description='Send command PostReject',#request_body=GetUserSerializer,
                             responses={201: NewActionSerializer, 400: 'Bad request'})
        def get(self, request,pk):
            #my_json = request.data
            return Response(
                action_helper.add_action(pk, 'scoring_complete_declined', 'user', payload="Отказано после скоринга"))


class PostAccept(APIView):
        @swagger_auto_schema(operation_description='Send command PostAccept', #request_body=GetUserSerializer,
                             responses={201: NewActionSerializer, 400: 'Bad request'})
        def get(self, request, pk):
            #my_json = request.data
            return Response(
                action_helper.add_action(pk, 'scoring_complete_accepted', 'user', payload="Одобрено после скоринга"))


class PreReject(APIView):
    @swagger_auto_schema(operation_description='Send command PreReject', request_body=RejectSerializer,
                         responses={201: NewActionSerializer, 400: 'Bad request'})
    def post(self, request, pk):
        my_json = request.data
        #User.objects.get(my_json['user_id'])
        return Response(action_helper.add_action(pk, 'manual_decline', 'user', my_json['payload']))


class ScoringStart(APIView):
    @swagger_auto_schema(operation_description='Send command ScoringStart', responses={201: NewActionSerializer,
                                                                                     400: 'Bad request'})
    def get(self, request, pk):
        action = action_helper.add_action(pk, 'scoring', 'user', payload="Пользователь запустил процесс скоринга")

        resp = json.dumps({'message_type': "individual_scoring_process",
                           'body': json.dumps({"individual_id": pk, "product_id": get_product_id_for_individual(pk)})})

        raw_data = api_requestor.post('/message/', resp)

        return Response(action)

