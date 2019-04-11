import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender
from portal.lib.willz_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.serializers.willz_serializer import *
from portal.models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


class MainAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = RawClientData.objects.all()
    serializer_class = RawClientDataSerializer


    @action(methods=['post'], detail=False, url_path='new')
    def new_data(self, request, pk=None):
        return Response(new_willz_client(request))


    @action(methods=['post'], detail=False, url_path='update')
    def update_data(self, request, pk=None):
        #делаем так:
        #отправляем сообщение на шину, но с обновлением client_raw_update
        #тогда процессор будет  искать виллза и потом делать пут. Для пута генерация +1.
        return Response(status=status.HTTP_200_OK)


