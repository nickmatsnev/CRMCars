import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender, api_requestor
from portal.lib.status_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.models import *


class MainApi(APIView):
    @swagger_auto_schema(operation_description='Get table of statuses', responses={200: StatusSerializer,
                                                                                   204: 'No content'})
    def get(self, request,):
        return get_status_table()

    @swagger_auto_schema(operation_description='Get clients for current status', request_body=GetStatusSerializer,
                            responses={200: GetStatusSerializer,
                                       400: 'No field status in request',
                                       204: 'No clients with current status'
                                       })
    def post(self, request):
        return get_clients_by_status(request.data)

