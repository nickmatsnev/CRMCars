import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender
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
from django.utils.encoding import uri_to_iri


class MainAPI(mixins.ListModelMixin,mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
              viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(methods=['get'], detail=False, url_path='view', serializer_class=ViewTableSerializer)
    def view_table_all(self, request, pk=None):
        return Response(get_all_clients_info())

    @action(methods=['get'], detail=True, url_path='view')
    def view_table(self, request, pk):
        return Response(get_current_client_info(pk))

    @action(methods=['post'], detail=True, url_path='update_product', serializer_class=ProductUpdateSerializer)
    def update_fields(self, request, pk):
        return update_product(request.data,pk)


class ClientApi(APIView):
    @swagger_auto_schema(operation_description='get all clients',
                         responses={200: ClientSerializer(many=True),
                                    404: 'No data'})
    def get(self, request):
        return Response(get_all_clients_info())

    @swagger_auto_schema(operation_description='post new client',
                         request_body=ClientSerializer,
                         responses={200: ClientSerializer,
                                    400: 'Format is not valid'})
    def post(self, request):
        return post_client(request.data)


class ClientPageApi(APIView):
    @swagger_auto_schema(operation_description='get all clients',
                         responses={200: ClientSerializer(many=True),
                                    404: 'No data'})
    def get(self, request, page):
        return Response(get_all_clients_info(page=page))


class ClientGetStatusApi(APIView):
    @swagger_auto_schema(operation_description='get all clients status' ,
                         responses={200: 'list of status and number of clients',
                                    404: 'No data'})
    def get(self, request):
        return Response(get_all_clients_status())


class ClientFilterApi(APIView):
    @swagger_auto_schema(operation_description='get all clients with filter by status or surname',
                         responses={200: ClientSerializer(many=True),
                                    404: 'No data'})
    def get(self, request, filter_status_or_surname):
        return Response(get_all_clients_info(uri_to_iri(filter_status_or_surname)))


class ClientFilterPageApi(APIView):
    @swagger_auto_schema(operation_description='get all clients with filter by status or surname',
                         responses={200: ClientSerializer(many=True),
                                    404: 'No data'})
    def get(self, request, filter_status_or_surname, page):
        return Response(get_all_clients_info(uri_to_iri(filter_status_or_surname),page=page))


class ClientWorkApi(APIView):
    @swagger_auto_schema(operation_description='get client',
                         responses={200: ClientSerializer,
                                    404: 'No data'})
    def get(self, request, id):
        return Response(get_current_client_info(id))


class UpdateClientWorkApi(APIView):
    @swagger_auto_schema(operation_description='post new client',
                         request_body=ClientSerializer,
                         responses={200: ClientSerializer,
                                    400: 'Format is not valid'})
    def post(self, request,id):
        return post_existing_client(request.data,id)


class UpdateProductApi(APIView):
    @swagger_auto_schema(operation_description='update product',
                         request_body=ProductUpdateSerializer,
                         responses={200: ProductUpdateSerializer,
                                    404: 'No data'})
    def post(self, request, id):
        return update_product(request.data, id)


