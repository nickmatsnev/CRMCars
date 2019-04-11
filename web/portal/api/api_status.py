import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender
from portal.lib.status_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.models import *
from core.lib.api import ApiRequestor
from portal.lib.product_api_helpers import get_product_id_for_individual
from django.contrib.auth.models import User


class MainApi(APIView):
    @swagger_auto_schema(operation_description='Get table of statuses', responses={200: StatusSerializer,
                                                                                   204: constants.NAME_NO_CONTENT})
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
                             responses={201: NewActionSerializer, 400: constants.NAME_BAD_REQUEST})
        def get(self, request,pk):
            #my_json = request.data
            return Response(
                ApiRequestor(request).add_action(pk, constants.NAME_SCORING_COMPLETE_DECLINED,constants.NAME_USER,
                                                 payload=constants.NAME_SCORING_COMPLETE_DECLINED_RU))


class PostAccept(APIView):
        @swagger_auto_schema(operation_description='Send command PostAccept', #request_body=GetUserSerializer,
                             responses={201: NewActionSerializer, 400: constants.NAME_BAD_REQUEST})
        def get(self, request, pk):
            # my_json = request.data
            return Response(
                ApiRequestor(request).add_action(pk, NAME_SCORING_COMPLETE_ACCEPTED, constants.NAME_USER,
                                                 payload=constants.NAME_SCORING_COMPLETE_ACCEPTED_RU))


class PreReject(APIView):
    @swagger_auto_schema(operation_description='Send command PreReject', request_body=RejectSerializer,
                         responses={201: NewActionSerializer, 400: constants.NAME_BAD_REQUEST})
    def post(self, request, pk):
        my_json = request.data
        #User.objects.get(my_json['user_id'])
        return Response(ApiRequestor(request).add_action(pk, constants.NAME_MANUAL_DECLINE, constants.NAME_USER, my_json['payload']))


class ScoringStart(APIView):
    @swagger_auto_schema(operation_description='Send command ScoringStart', responses={201: NewActionSerializer,
                                                                                     400: constants.NAME_BAD_REQUEST})
    def get(self, request, pk):
        action = ApiRequestor(request).add_action(pk, constants.NAME_SCORING, constants.NAME_USER,
                                                  payload=constants.NAME_SCORING_RU)

        resp = json.dumps({constants.NAME_MESSAGE_TYPE: constants.NAME_INDIVIDUAL_SCORING_PROCESS,
                           constants.NAME_BODY: json.dumps({"individual_id": pk, "product_id": get_product_id_for_individual(pk)})})
        ApiRequestor(request).send_message(resp)

        return Response(action)

