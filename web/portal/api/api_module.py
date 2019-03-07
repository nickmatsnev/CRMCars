import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response
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


class ModuleDataApi(APIView):
    @swagger_auto_schema(operation_description='Get module data is it is', responses={200: ModuleDataSerializer})
    def get(self, request, pk,module_type):
        queryset = ModuleData.objects.filter(individual=pk,type=module_type).first()
        serializer_class = ModuleDataSerializer(queryset,many=False)
        return Response(serializer_class.data)

#TODO: нет проверки типа модуля при создании!
    @swagger_auto_schema(operation_description='Update module data', request_body=ModuleUpdateDataSerializer)
    def post(self, request, pk,module_type):
        json_data = request.data
        queryset = ModuleData.objects.create(type=module_type,individual=pk,raw_data=json_data['raw_data'])
        serializer_class = ModuleDataSerializer(queryset,many=False)
        return Response(serializer_class.data)



class GetModuleApi(APIView):
    @swagger_auto_schema(operation_description='Get module as it is', responses={200: SourceGetModuleSerializer})
    def get(self, request, module_type):
        return Response(get_module_by_type(module_type))

  #  @swagger_auto_schema(operation_description='Get module as it is', request_body=SourceGetModuleSerializer)
  #  def post(self, request, module_type):

    #    return Response(post_test(module_type,request))

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
    @swagger_auto_schema(operation_description='GetModule by name and type')
    def get(self, request, module_type, pk):
        return Response(get_module_by_type(module_type, pk))

class GetModuleByNameApi(APIView):
    @swagger_auto_schema(operation_description='Send message to message bus')
    def get(self, request, module_type,module_name):
        return Response(get_module_by_name(module_type,module_name))


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


class CredentialsApi(APIView):
    @swagger_auto_schema(operation_description='Get credentials',
                         responses={200: CredentialsSerializer,
                                    204: 'No module with your ID',
                                    400: 'No source module with your ID'})
    def get(self, request, id):
        module_type = 'source'
        return get_credentials(module_type,id)

    @swagger_auto_schema(operation_description='Set credentials',
                         request_body=CredentialsSerializer,
                         responses={200: CredentialsSerializer,
                                    204: 'No module with your ID',
                                    400: 'No source module with your ID'})
    def post(self, request,id):
        module_type = 'source'
        return Response(set_credentials(module_type,id,request.data['credentials']))





