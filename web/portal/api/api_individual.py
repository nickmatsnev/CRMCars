
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
from portal.lib.module_api_helpers import get_generation_number
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

        response_data['status'] = get_status(individual.id)

        generations = Generation.objects.filter(individual_id=individual.id)
        response_data['generations_count'] = generations.count()

        current_generation = generations.filter(number=get_generation_number(individual.id, 'current')).get()

        generation_serializer = GenerationGetSerializer(current_generation, many = False)
        response_data['current_generation'] = generation_serializer.data

        client = individual.client
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
    def post(self, request, pk, generation_id_or_current_generation):
        return new_action(request.data, pk, get_generation_number(pk, generation_id_or_current_generation))


class CurGenApi(APIView):
    @swagger_auto_schema(operation_description='Current generation',
                         responses={200: 'integer',
                                    204: 'no valid generations'})
    def get(self, request, pk):
        gen_number = get_generation_number(pk,'current')
        if gen_number != 0:
            return Response(data=gen_number)
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
        action_model = Action.objects.create(generation=new_gen, create_time=datetime.datetime.now(),
                                             processor='system',action_type='new')
        return Response(new_gen.number)


class GenApi(APIView):
    @swagger_auto_schema(operation_description='List of all generations',
                         responses={200: 'List'})
    def get(self, request, pk):
        generations = Generation.objects.filter(individual_id=pk)
        generations_serializer = GenerationGetSerializer(generations,many=True)
        return Response(generations_serializer.data)

