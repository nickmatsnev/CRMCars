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
from rest_framework.parsers import FormParser,MultiPartParser

import json
import pika

from rest_framework.renderers import JSONRenderer
from core.lib import constants
from rest_framework import viewsets
from core.lib import api_requestor
from core.lib import module

class UserListApi(mixins.ListModelMixin, mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClientsListApi(APIView):

    @swagger_auto_schema(operation_description='GET /front/clients/')
    def get(self, request):
        items = []
        try:
            clients = Client.objects.all()
            cntr = 0
            for client in clients:
                for individual in client['individuals']:
                    if individual['primary'] == True:
                        new_item = {}
                        new_item['fio'] = individual['first_name'] + ' ' + individual['last_name']
                        cntr += 1
                        new_item['num'] = cntr
                        new_item['id'] = client['id']
                        new_item['created_at'] = client['created_at']
                        new_item['status'] = get_status(individual['id'])

                        items.append(new_item)
        except:
            new_item = {}
            items = new_item
        finally:
            return Response(items)


class ClientInspectApi(APIView):

    @swagger_auto_schema(operation_description='GET /front/clients/<int:id>/')
    def get(self, request, pk):
        queryset = Client.objects.get(id=pk)
        serializer = ClientGetSerializer(queryset, many=False)

        individual = {}
        drivers = []
        for individual_raw in serializer.data['individuals']:
            driver ={}
            driver['name']=individual_raw['first_name']
            driver['surname'] = individual_raw['last_name']
            driver['number'] = individual_raw['driver_license']['number']
            driver['issued_at'] = individual_raw['driver_license']['issued_at']
            driver['primary'] = individual_raw['primary']
            if individual_raw['primary'] == True:
                individual = individual_raw

            drivers.append(driver)

        op_history = []
        queryset = Generation.objects.get(individual_id=individual['id'])
        serializer = GenerationSerializer(queryset, many=False)
        op_history = serializer.data

        items = {}
        items['id'] = pk
        items['individual'] = individual
        items['drivers'] = drivers
        items['op_history'] = op_history

        return Response(items)


def get_status(individual_id):
    gen_data = api_requestor.request('/generation/{0}'.format(individual_id))
    source_cnt = 0
    check_cnt = 0
    scorint_cnt = 0
    declined = False
    accepted = False
    new = False

    for act in gen_data['actions']:
        if act['action_type'] == 'declined':
            declined =  True
        if act['action_type'] == 'accepted':
            accepted = True
        if act['action_type'] == 'new':
            new = True


    # определить что выше по приоритетам!
    if declined==True:
        return 'Отказано'
    if accepted==True:
        return 'Одобрено'

    if new == True:
        return 'Новый'

    return 'Неизвестно'


# TODO: Не было тестирования этой части
class ParserGetActiveAPI(APIView):
    @swagger_auto_schema(operation_description='Get active parameters',
                        responses={200: 'Table: source,parser,name,description,type'})
    def get(self, request):
        response_data = ""
        try:
            parsing_modules_parameters=[]
            parsing_modules = Module.objects.filter(type='Parser',is_active=True)
            for parsing_module in parsing_modules:
                parser_m = module.ParserModule(parsing_module.path)
                parameters = parser_m.get_parameters_meta()
                for parameter in parameters:
                    new_item = {}
                    new_item['source'] = parser_m.get_source()
                    new_item['parser'] = parser_m.get_module_name()
                    new_item['name'] = parameter['name']
                    new_item['description'] = parameter['description']
                    new_item['type'] = parameter['type']
                    parsing_modules_parameters.append(new_item)

            response_data = parsing_modules_parameters
        except:
            new_item = {}
            response_data = new_item
        finally:
            return Response(response_data)


class ParserGetAllAPI(APIView):
    @swagger_auto_schema(operation_description='Get all parsers',
                            responses={200: 'Table: name,path,is_active,creation_time'})
    def get(self, request):
        response_data = ""
        try:
            parsing_modules = Module.objects.filter(type='Parser')
            items=[]
            for parsing_module in parsing_modules:
                item = {}
                item['name'] = parsing_module.name
                item['path'] = parsing_module.path
                item['is_active'] = parsing_module.is_active
                item['creation_time'] = parsing_module.create_time
                items.append(item)

            response_data = items
        except:
            item = {}
            response_data = item
        finally:
            return Response(response_data)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class ParserUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    #@swagger_auto_schema(operation_description='Parser upload API',
     #                    request_body=openapi.Schema(type=openapi.TYPE_STRING, description='.py file'))

    def post(self, request, format='py'):
        current_status = status.HTTP_201_CREATED
        try:
            uploaded_file = request.FILES['file']
            path = "../core/parsers/"
            destination = open(path + uploaded_file.name, 'wb+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()

            item = {}
            item['name']= uploaded_file.name
            item['path']= path
            serializer = ScoringModuleSerializer(data=item)

            if serializer.is_valid():
                resp_data = serializer.save()
        except:
            current_status = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(status = current_status)


# TODO: Не было тестирования этой части
class ScoringGetActiveAPI(APIView):
    @swagger_auto_schema(operation_description='Get active parameters',
                        responses={200: 'Table: source,parser,name,description,type'})
    def get(self, request):
        response_data = ""
        try:
            parsing_modules_parameters=[]
            parsing_modules = Module.objects.filter(type='Scoring',is_active=True)
            for parsing_module in parsing_modules:
                parser_m = module.ParserModule(parsing_module.path)
                parameters = parser_m.get_parameters_meta()
                for parameter in parameters:
                    new_item = {}
                    new_item['source'] = parser_m.get_source()
                    new_item['parser'] = parser_m.get_module_name()
                    new_item['name'] = parameter['name']
                    new_item['description'] = parameter['description']
                    new_item['type'] = parameter['type']
                    parsing_modules_parameters.append(new_item)

            response_data = parsing_modules_parameters
        except:
            new_item = {}
            response_data = new_item
        finally:
            return Response(response_data)


class ScoringGetAllAPI(APIView):
    @swagger_auto_schema(operation_description='Get all scorings',
                            responses={200: 'Table: name,path,is_active,creation_time'})
    def get(self, request):
        response_data = ""
        try:
            scoring_modules = Module.objects.filter(type='Scoring')
            items=[]
            for scoring_module in scoring_modules:
                item = {}
                item['name'] = scoring_module.name
                item['path'] = scoring_module.path
                item['is_active'] = scoring_module.is_active
                item['creation_time'] = scoring_module.create_time
                items.append(item)

            response_data = items
        except:
            item = {}
            response_data = item
        finally:
            return Response(response_data)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class ScoringUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    #@swagger_auto_schema(operation_description='Parser upload API',
     #                    request_body=openapi.Schema(type=openapi.TYPE_STRING, description='.py file'))

    def post(self, request, format='py'):
        current_status = status.HTTP_201_CREATED
        try:
            uploaded_file = request.FILES['file']
            path = "../core/scorings/"
            destination = open(path + uploaded_file.name, 'wb+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()

            item = {}
            item['name']= uploaded_file.name
            item['path']= path
            serializer = ScoringModuleSerializer(data=item)

            if serializer.is_valid():
                resp_data = serializer.save()
        except:
            current_status = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(status = current_status)


# TODO: Не было тестирования этой части
class SourceGetActiveAPI(APIView):
    @swagger_auto_schema(operation_description='Get active parameters',
                        responses={200: 'Table: source,parser,name,description,type'})
    def get(self, request):
        response_data = ""
        try:
            parsing_modules_parameters=[]
            parsing_modules = Module.objects.filter(type='Source',is_active=True)
            for parsing_module in parsing_modules:
                parser_m = module.ParserModule(parsing_module.path)
                parameters = parser_m.get_parameters_meta()
                for parameter in parameters:
                    new_item = {}
                    new_item['source'] = parser_m.get_source()
                    new_item['parser'] = parser_m.get_module_name()
                    new_item['name'] = parameter['name']
                    new_item['description'] = parameter['description']
                    new_item['type'] = parameter['type']
                    parsing_modules_parameters.append(new_item)

            response_data = parsing_modules_parameters
        except:
            new_item = {}
            response_data = new_item
        finally:
            return Response(response_data)


class SourceGetAllAPI(APIView):
    @swagger_auto_schema(operation_description='Get all sources',
                            responses={200: 'Table: name,path,is_active,creation_time,credentials'})
    def get(self, request):
        response_data = ""
        try:
            source_modules = Module.objects.filter(type='Scoring')
            items=[]
            for source_module in source_modules:
                item = {}
                item['name'] = source_module.name
                item['path'] = source_module.path
                item['is_active'] = source_module.is_active
                item['creation_time'] = source_module.create_time
                item['credentials'] = source_module.credentials
                items.append(item)

            response_data = items
        except:
            item = {}
            response_data = item
        finally:
            return Response(response_data)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class SourceUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    #@swagger_auto_schema(operation_description='Parser upload API',
     #                    request_body=openapi.Schema(type=openapi.TYPE_STRING, description='.py file'))

    def post(self, request, format='py'):
        current_status = status.HTTP_201_CREATED
        try:
            uploaded_file = request.FILES['file']
            path = "../core/sources/"
            destination = open(path + uploaded_file.name, 'wb+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()

            item = {}
            item['name']= uploaded_file.name
            item['path']= path
            serializer = SourceModuleSerializer(data=item)

            if serializer.is_valid():
                resp_data = serializer.save()
        except:
            current_status = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(status = current_status)
