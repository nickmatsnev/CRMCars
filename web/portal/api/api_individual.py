
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
    @swagger_auto_schema(operation_description='Get individual by ID with generation',
                         responses={200: IndividualGetGenerationSerializer})
    def get(self, request, pk):
        individual = Individual.objects.get(id=pk)
        individual_serializer = IndividualGetSerializer(individual, many=False)
        response_data = individual_serializer.data
        client = individual.client
        generation = Generation.objects.filter(individual=pk)
        generation_serializer = GenerationGetSerializer(generation, many = True)
        response_data['generations'] = generation_serializer.data

        product = Product.objects.get(id=client.product)
        if individual.primary == True:
            module_id = product.primary_scoring
        else:
            module_id = product.other_scoring

        scoring_module = Module.objects.filter(pk=module_id)
        if scoring_module.count() != 0:
            scoring_module = Module.objects.get(pk=module_id)
            response_data['scoring_model'] = scoring_module.name
            response_data['scoring_model_id'] = scoring_module.id
        else:
            response_data['scoring_model'] = "Not set"
            response_data['scoring_model_id'] = 0
        return Response(response_data)


class AddActionApi(APIView):
    @swagger_auto_schema(operation_description='Add action',
                         request_body=NewActionSerializer,
                         responses={201: NewActionSerializer,
                                    400: 'Bad request'})
    def post(self, request, pk, generation):
        return new_action(request.data, pk, generation)


class CurGenApi(APIView):
    @swagger_auto_schema(operation_description='Current generation',
                         responses={200: 'integer',
                                    204: 'no valid generations'})
    def get(self, request, pk):
        generations = Generation.objects.filter(individual_id=pk)
        for gen in generations:
            if gen.is_archive==False:
                return Response(gen.number)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewGenApi(APIView):
    @swagger_auto_schema(operation_description='New generation',
                         responses={201: 'Created'})
    def get(self, request, pk):
        generations = Generation.objects.filter(individual_id=pk)
        last = 0
        for gen in generations:
            if gen.is_archive==False:
                last = gen.number
                gen.is_archive=True
                gen.save()

        individual = Individual.objects.get(pk=pk)
        last += 1
        new_gen = Generation.objects.create(individual=individual, number=last, create_time=datetime.datetime.now(),
                                      is_archive=False)
        return Response(new_gen.number)


class GenApi(APIView):
    @swagger_auto_schema(operation_description='List of all generations',
                         responses={200: 'List'})
    def get(self, request, pk):
        generations = Generation.objects.filter(individual_id=pk)
        generations_serializer = GenerationGetSerializer(generations,many=True)
        return Response(generations_serializer.data)

