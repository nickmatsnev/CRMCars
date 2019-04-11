import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender
from portal.lib.product_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.serializers.product_serializer import *
from portal.serializers.client_serializer import *
from portal.serializers.module_serializer import  *
from portal.models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


class MainAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
              viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['get'], detail=False, url_path='view', serializer_class=ViewTableSerializer)
    def view_table_all(self, request, pk=None):
        return Response(get_all_products_info())


