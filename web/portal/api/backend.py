from django.contrib.sites import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg import openapi

from core.lib import message_sender, api_requestor
from web.portal.serializers.backend import *
from web.portal.models import *

import json
import pika

from core.lib import module
from core.lib import process

from web.portal.serializers import *

from rest_framework import viewsets


class GenerationApi(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Generation.objects.all()
    serializer_class = GenerationSerializer


class ClientApi(mixins.ListModelMixin,mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientGetSerializer


class CreateClientApi(mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


#    @action(detail=False, renderer_classes=[renderers.StaticHTMLRenderer])
#    def test_method(self, request, myparam=None):
#        snippet = self.get_object()
#        return Response(snippet.highlighted)


class IndividualsApi(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer


class PassportsApi(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer


class DriverLicesesApi(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = DriverLicense.objects.all()
    serializer_class = DriverLicenseSerializer


class ImagesApi(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class RawClientDataApi(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = RawClientData.objects.all()
    serializer_class = RawClientDataSerializer


#class ScoringModelsApi(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#    queryset = ScoreModel.objects.all()
#    serializer_class = ScoreModelSerializer


class NewActionApi(APIView):
    @swagger_auto_schema(operation_description='Create new action',
                         request_body=NewActionSerializer)
    def post(self, request):
        raw_data = request.data
        generation = Generation.objects.get(individual_id=raw_data['individual'])
        action = Action.objects.create(generation=generation, processor=raw_data['processor'],
                                           action_type=raw_data['action_type'],
                                           payload=raw_data['payload'],
                                           create_time=datetime.datetime.now())
        action.save()
        return Response(status=status.HTTP_201_CREATED)


class BusMessageAPI(APIView):
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



class WillzCreateClient(APIView):
    @swagger_auto_schema(operation_description='Create new Willz client from raw_data',
                         request_body=openapi.Schema(type=openapi.TYPE_STRING, description='Raw JSON from Willz'))
    def post(self, request):
        raw_json = json.dumps(request.data)
        my_json = {"payload": raw_json}
        serializer = RawClientDataSerializer(data=my_json)

        if serializer.is_valid():
            resp_data = serializer.save()
            resp = json.dumps({'message_type': constants.CLIENT_RAW_CREATED_MESSAGE,
                               'body': json.dumps({'raw_client_id': resp_data.id})});

            raw_data = api_requestor.post('/bus_message/', resp)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# *** PARSER METHODS ***
class ParserGetAPI(APIView):
    @swagger_auto_schema(operation_description='Get current module',
                        responses={200: ParserGetModuleSerializer,
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            parsing_module = Module.objects.get(id=pk, type='Parser')
            serializer = ParserGetModuleSerializer(parsing_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


class ParserActivateAPI(APIView):
    @swagger_auto_schema(operation_description='Activate current module',
                        responses={200: 'Activated',
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            parsing_module = Module.objects.get(id=pk, type='Parser')
            parsing_module.is_active = True
            parsing_module.save()
            serializer = ParserGetModuleSerializer(parsing_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


class ParserDeactivateAPI(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module',
                        responses={200: 'Deactivated',
                                204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            parsing_module = Module.objects.get(id=pk, type='Parser')
            parsing_module.is_active = False
            parsing_module.save()
            serializer = ParserGetModuleSerializer(parsing_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class ParserGetParametersAPI(APIView):
    @swagger_auto_schema(operation_description='Get parameters',
                        responses={200: 'Parameters',
                                    204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            parsing_module = Module.objects.get(id=pk, type='Parser')
            load = module.ParserModule(parsing_module.path)
            parameters = load.get_parameters_meta()

            response_data = parameters
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


# *** SCORING METHODS ***
class ScoringGetAPI(APIView):
    @swagger_auto_schema(operation_description='Get current module',
                        responses={200: ScoringGetModuleSerializer,
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            scoring_module = Module.objects.get(id=pk, type='Scoring')
            serializer = ScoringGetModuleSerializer(scoring_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


class ScoringActivateAPI(APIView):
    @swagger_auto_schema(operation_description='Activate current module',
                        responses={200: 'Activated',
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            scoring_module = Module.objects.get(id=pk, type='Scoring')
            scoring_module.is_active = True
            scoring_module.save()
            serializer = ParserGetModuleSerializer(scoring_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


class ScoringDeactivateAPI(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module',
                        responses={200: 'Deactivated',
                                204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            scoring_module = Module.objects.get(id=pk, type='Scoring')
            scoring_module.is_active = False
            scoring_module.save()
            serializer = ParserGetModuleSerializer(scoring_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class ScoringGetParametersAPI(APIView):
    @swagger_auto_schema(operation_description='Get parameters',
                        responses={200: 'Parameters',
                                    204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            scoring_module = Module.objects.get(id=pk, type='Scoring')
            load = module.ParserModule(scoring_module.path)
            parameters = load.get_parameters_meta()

            response_data = parameters
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


# *** SOURCE METHODS ***
class SourceGetAPI(APIView):
    @swagger_auto_schema(operation_description='Get current module',
                        responses={200: SourceGetModuleSerializer,
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            source_module = Module.objects.get(id=pk, type='Source')
            serializer = SourceGetModuleSerializer(source_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


class SourceActivateAPI(APIView):
    @swagger_auto_schema(operation_description='Activate current module',
                        responses={200: 'Activated',
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            source_module = Module.objects.get(id=pk, type='Source')
            source_module.is_active = True
            source_module.save()
            serializer = SourceGetModuleSerializer(source_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


class SourceDeactivateAPI(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module',
                        responses={200: 'Deactivated',
                                204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            source_module = Module.objects.get(id=pk, type='Source')
            source_module.is_active = False
            source_module.save()
            serializer = SourceGetModuleSerializer(source_module, many=False)
            response_data = serializer.data
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class SourceGetParametersAPI(APIView):
    @swagger_auto_schema(operation_description='Get parameters',
                        responses={200: 'Parameters',
                                    204: 'No module with such PK'})
    def get(self, request, pk):
        current_status = status.HTTP_200_OK
        response_data = ""

        try:
            source_module = Module.objects.get(id=pk, type='Source')
            load = module.ParserModule(source_module.path)
            parameters = load.get_parameters_meta()

            response_data = parameters
        except:
            current_status=status.HTTP_204_NO_CONTENT
        finally:
            return Response(status=current_status,data=response_data)


#class GenerationCreateApi(mixins.CreateModelMixin,
#                    viewsets.GenericViewSet):
#    queryset = Generation.objects.all()
#    serializer_class = GenerationCreateSerializer


#class GenerationGetAllApi(APIView):
#    def get_object(self, pk):
#        try:
#            return Generation.objects.filter(individual=pk)[0]
#        except Individual.DoesNotExist:
#            raise Http404

#    @swagger_auto_schema(operation_description='Used to get all generations for individual')
#    def get(self, request, pk, *args, **kwargs):
#        queryset = self.get_object(pk)
#        serializer = GenerationGetSerializer(queryset)
#        return Response(serializer.data)


#class GenerationGetTasksApi(APIView):
#    def get_object(self, pk):
#        try:
#            return Generation.objects.filter(individual=pk)[0]
#        except Individual.DoesNotExist:
#            raise Http404

#    @swagger_auto_schema(operation_description='Used to get all tasks for individual')
#    def get(self, request, pk, *args, **kwargs):
#        queryset = self.get_object(pk)
#        serializer = GenerationGetSerializer(queryset)
#        return Response(serializer.data)

# class start_task(APIView):
#     def get(self,reque        r = requests.post('https://www.somedomain.com/some/url/save', params=request.POST)st):
#         #дописать
#         return Response(status=status.HTTP_200_OK)
#
#
# class finalize_task(APIView):
#     def get(self,request):
#         task_id = self.request.query_params.get('task_id', None)
#         if task_id is not None:
#             #не пойму какую таблицу юзать
#             task_table = Task.objects.filter(task=task_id)
#             task_table.task_status =2
#             task_table.save
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
# class create_passport(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = PassportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_license(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = LicenseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_individual(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = IndividualSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_image(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_client(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = ClientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class update_client_task_data(APIView):
#     def get(self,request):
#         task_id = self.request.query_params.get('task_id', None)
#         client_id = self.request.query_params.get('client_id', None)
#
#         if task_id and client_id is not None:
#             task_table = ClientTask.objects.filter(task=task_id)
#             task_table.client = client_id
#             task_table.save
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
# class get_default_score_model(APIView):
#     def get(self,request):
#         return JsonResponse({'score_model id': '1'})
#
#
# class get_sources(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class get_individual_passport(APIView):
#     def get(self,request):
#         queryset = PassportSerializer.objects.all()
#         individual_id = self.request.query_params.get('individual_id', None)
#         if individual_id is not None:
#             queryset = queryset.filter(individual_id=individual_id)
#             return queryset
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# class get_individual_license(APIView):
#     def get(self,request):
#         queryset = LicenseSerializer.objects.all()
#         individual_id = self.request.query_params.get('individual_id', None)
#         if individual_id is not None:
#             queryset = queryset.filter(individual_id=individual_id)
#             return queryset
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_source_raw_data(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class update_source_task(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class get_source_raw_data_for_individual(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class insert_check(APIView):
#     def get(self,request):
#         individual_id = self.request.query_params.get('individual_id', None)
#         value = self.request.query_params.get('value', None)
#         check_registry_id = self.request.query_params.get('check_registry_id', None)
#
#         if individual_id and value and check_registry_id is not None:
#             check_table = Check.objects.filter(individual=individual_id,checkRegistry=check_registry_id)
#             check_table.value = value
#             check_table.save
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
