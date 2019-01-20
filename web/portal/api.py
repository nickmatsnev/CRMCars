from django.contrib.sites import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg import openapi
from web.portal.serializers import RawClientDataSerializer
from django.http import Http404

import json
import pika

from core.lib import constants

from web.portal.serializers import *

from rest_framework import viewsets

class ClientApi(mixins.CreateModelMixin,
                mixins.ListModelMixin,
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


class GetClientApi(APIView):

    @swagger_auto_schema(operation_description='Used to get current client')
    def get(self, request, pk, *args, **kwargs):
        obj = Client.objects.get(pk=pk)
        client = ClientSerializer(obj)

        json_info = client.data

        queryset = Individual.objects.filter(client_id=json_info['id'])
        individuals = IndividualSerializer(queryset, many=True)
        json_info['individuals'] = individuals.data

        k = 0
        for individual in json_info['individuals']:
            where_id = individual['id']
            passport_obj = Passport.objects.get(individual_id=where_id)
            passport = PassportSerializer(passport_obj)
            psp_where_id = passport.data['id']
            json_info['individuals'][k]['Passport'] = passport.data

            img_objs = Image.objects.filter(individual_id=where_id,passport_id=psp_where_id)
            images = ImageSerializer(img_objs, many=True)
            json_info['individuals'][k]['Passport']['Images'] = images.data

            driver_license_obj = DriverLicense.objects.get(individual_id=where_id)
            driver_license = DriverLicenseSerializer(driver_license_obj)
            drv_where_id = driver_license.data['id']
            json_info['individuals'][k]['DriverLicense'] = driver_license.data

            img_objs = Image.objects.filter(individual_id=where_id,driver_license=drv_where_id)
            images = ImageSerializer(img_objs, many=True)
            json_info['individuals'][k]['DriverLicense']['Images'] = images.data
            k += 1

        #return Response(data=json.dumps(json_info,ensure_ascii=False).encode('utf8'))
        return Response(data=json_info)

class GetPrimaryIndividual(APIView):
    def get_object(self, pk):
        try:
            return Individual.objects.filter(client=pk)[0]
        except Individual.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='Used to get Primary Individual for current client')
    def get(self, request, pk, *args, **kwargs):
        queryset = self.get_object(pk)
        serializer = IndividualSerializer(queryset)
        return Response(serializer.data)


class WillzCreateClient(APIView):
    @swagger_auto_schema(operation_description='POST /api/willz/',
                         request_body=openapi.Schema(type=openapi.TYPE_STRING, description='Raw JSON from Willz'))
    def post(self, request):
        raw_json = json.dumps(request.data)
        my_json = {"payload": raw_json}
        serializer = RawClientDataSerializer(data=my_json)

        if serializer.is_valid():
            resp_data = serializer.save()
            resp = json.dumps({'raw_client_id': resp_data.id})
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            channel = connection.channel()
            channel.basic_publish(constants.MAIN_EXCHANGE_NAME,
                                  routing_key=constants.CLIENT_RAW_CREATED_MESSAGE,
                                  body=resp, properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))
            connection.close()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RawClientData(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = RawClientData.objects.all()
    serializer_class = RawClientDataSerializer


class ScoringModelsApi(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ScoreModel.objects.all()
    serializer_class = ScoreModelSerializer


class TasksModelApi(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ClientTaskApi(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = ClientTask.objects.all()
    serializer_class = ClientTaskSerializer


class UpdateClientTaskApi(APIView):
        def get_object(self, pk):
            try:
                return ClientTask.objects.get(pk=pk)
            except Individual.DoesNotExist:
                raise Http404

        @swagger_auto_schema(operation_description='Update task by ID',
                             request_body=ClientTaskSerializer)
        def post(self, request, pk, *args, **kwargs):
            queryset = self.get_object(pk)
            serializer = ClientTaskSerializer(queryset)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerationCreateApi(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Generation.objects.all()
    serializer_class = GenerationCreateSerializer


class GenerationGetAllApi(APIView):
    def get_object(self, pk):
        try:
            return Generation.objects.filter(individual=pk)[0]
        except Individual.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='Used to get all generations for individual')
    def get(self, request, pk, *args, **kwargs):
        queryset = self.get_object(pk)
        serializer = GenerationGetSerializer(queryset)
        return Response(serializer.data)


class GenerationGetTasksApi(APIView):
    def get_object(self, pk):
        try:
            return Generation.objects.filter(individual=pk)[0]
        except Individual.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='Used to get all tasks for individual')
    def get(self, request, pk, *args, **kwargs):
        queryset = self.get_object(pk)
        serializer = GenerationGetSerializer(queryset)
        return Response(serializer.data)

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
