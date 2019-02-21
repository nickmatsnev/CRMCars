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


class MainAPI(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
              viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(methods=['get'], detail=False, url_path='view', serializer_class=ViewTableSerializer)
    def view_table_all(self, request, pk=None):
        return Response(get_all_clients_info())

    @action(methods=['get'], detail=True, url_path='view')
    def view_table(self, request, pk):
        return Response(get_current_client_info(pk))

    @action(methods=['post'], detail=True, url_path='add_action', serializer_class = NewActionSerializer)
    def add_action(self, request, pk):
        return Response(new_action(request.data,pk))

    @action(methods=['post'], detail=True, url_path='update_product', serializer_class=ProductUpdateSerializer)
    def update_fields(self, request, pk):
        return Response(update_product(request.data,pk))


