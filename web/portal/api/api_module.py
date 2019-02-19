import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender, api_requestor
from portal.lib.module_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.serializers.module_serializer import *
from portal.models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from rest_framework.parsers import FormParser,MultiPartParser


class GetModuleApi(APIView):
    @swagger_auto_schema(operation_description='Get module as it is', responses={200: SourceGetModuleSerializer})
    def get(self, request, module_type):
        return Response(get_module_by_type(module_type))


class ViewModuleApi(APIView):
    @swagger_auto_schema(operation_description='Get module in a table view')
    def get(self, request, module_type):
        return Response(view_module_by_type(module_type))


class GetViewParametersApi(APIView):
    @swagger_auto_schema(operation_description='Get module parameters in a table view')
    def get(self, request, module_type):
        return Response(view_all_parameters_from_active_modules(module_type))


class UploadModuleApi(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(operation_description='Module upload API')
     #                    request_body=openapi.Schema(type=openapi.TYPE_STRING, description='.py file'))
    def post(self, request, module_type):
       return Response(save_module(request, module_type))


class GetModuleByIdApi(APIView):
    @swagger_auto_schema(operation_description='Send message to message bus')
    def get(self, request, module_type,id):
        return Response(get_module_by_type(module_type,id))


class GetModuleParametersByIdApi(APIView):
    @swagger_auto_schema(operation_description='Get parameters of current module')
    def get(self, request, module_type,id):
        return Response(get_module_parameters(module_type,id))


class ActivateApi(APIView):
    @swagger_auto_schema(operation_description='Acivate current module')
    def get(self, request, module_type,id):
        return Response(set_module_is_active_by_id_type(module_type,id,True))


class DeactivateApi(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module')
    def get(self, request, module_type,id,active_module):
        return Response(set_module_is_active_by_id_type(module_type,id,False))