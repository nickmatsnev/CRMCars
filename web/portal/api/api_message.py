import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender, basic_api_requestor
from core.lib.modules import ScoringModule, SourceModule
from portal.serializers.message_serializer import *
from portal.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from core.lib import action_helper

class MainApi(APIView):
    @swagger_auto_schema(operation_description='Send message to message bus',
                         request_body=BusMessageSerializer)
    def post(self, request):
        raw_data = request.data
        serializer = BusMessageSerializer(data=raw_data)
        if serializer.is_valid():
            message_sender.send_message(message_code=serializer.validated_data['message_type'],
                                        body=serializer.validated_data['body'])
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class TestApi(APIView):
    @swagger_auto_schema(operation_description='For testing some functions')
    def get(self, request):
        action_helper.add_action_individual(1,"qwerty","zh")
        return Response(status=status.HTTP_200_OK)

