
import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender, api_requestor
from portal.lib.client_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.serializers.client_serializer import *
from portal.serializers.product_serializer import *
from portal.serializers.module_serializer import  *
from portal.models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


class MainApi(APIView):
    @swagger_auto_schema(operation_description='Get individual by ID with generation', responses={200: IndividualGetGenerationSerializer})
    def get(self, request, pk):
        individual = Individual.objects.get(id=pk)
        individual_serializer = IndividualGetSerializer(individual, many=False)
        response_data = individual_serializer.data
        client = individual.client
        generation = Generation.objects.get(client=client)
        generation_serializer = GenerationGetSerializer(generation, many = False)
        response_data['generation'] = generation_serializer.data
        response_data['client'] = client.id

        return Response(response_data)

