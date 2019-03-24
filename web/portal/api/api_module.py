import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from core.lib import message_sender, basic_api_requestor
from portal.lib.module_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from rest_framework.parsers import FormParser, MultiPartParser
from portal.serializers.module_serializer import *


class ModuleDataApi(APIView):
    @swagger_auto_schema(operation_description='Get module data is it is',
                         responses={200: "raw data",
                                    204: "No module"})
    def get(self, request, pk, module_type, module_name, gen_id_or_cur_gen):
        return get_module_data_by_type_name(pk, module_type, module_name, get_generation_number(pk, gen_id_or_cur_gen))

    @swagger_auto_schema(operation_description='Update/Create module data', request_body=ModuleUpdateDataSerializer,
                         responses={201: "Module created",
                                    202: "Module updated",
                                    400: "No module with requested name"})
    def post(self, request, pk, module_type, module_name, gen_id_or_cur_gen):
        return set_module_data_by_type_name(request.data, pk, module_type, module_name,
                                            get_generation_number(pk, gen_id_or_cur_gen))


class ModuleMetaApi(APIView):
    @swagger_auto_schema(operation_description='Get module data is it is',
                         responses={200: ModuleMetaSerializer,
                                    204: "No module"})
    def get(self, request, pk, module_type, module_name, gen_id_or_cur_gen):
        return get_module_meta_by_type_name(pk, module_type, module_name, get_generation_number(pk, gen_id_or_cur_gen))


class ModuleDataListApi(APIView):
    @swagger_auto_schema(operation_description='Get module data is it is',
                         responses={200: ModuleDataListSerializer,
                                    204: "No data"})
    def get(self, request, pk, module_type, gen_id_or_cur_gen):
        return get_module_data_list_by_type(pk, module_type, get_generation_number(pk, gen_id_or_cur_gen))


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

    @swagger_auto_schema(operation_description='Module upload', responses={201: "Module uploaded",
                                                                           400: "Unknown error",
                                                                           202: "Module updated"})
    def post(self, request, module_type):
        return save_module(request, module_type)


class DeleteModuleApi(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(operation_description='Module delete',
                         responses={200: "Module <module_name> deleted successfully",
                                    204: "Not found"})
    def get(self, request, module_type, module_name):
        return delete_module(module_type, module_name)


class GetModuleByIdApi(APIView):
    @swagger_auto_schema(operation_description='GetModule by name and type')
    def get(self, request, module_type, pk):
        return Response(get_module_by_type(module_type, pk))


class GetModuleByNameApi(APIView):
    @swagger_auto_schema(operation_description='Send message to message bus')
    def get(self, request, module_type, module_name):
        return Response(get_module_by_name(module_type, module_name))


class GetModuleParametersByIdApi(APIView):
    @swagger_auto_schema(operation_description='Get parameters of current module')
    def get(self, request, module_type, id):
        return Response(get_module_parameters(module_type, id))


class ActivateApi(APIView):
    @swagger_auto_schema(operation_description='Acivate current module')
    def get(self, request, module_type, id):
        return Response(set_module_is_active_by_id_type(module_type, id, True))


class DeactivateApi(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module')
    def get(self, request, module_type, id, active_module):
        return Response(set_module_is_active_by_id_type(module_type, id, False))


class CredentialsApi(APIView):
    @swagger_auto_schema(operation_description='Get credentials',
                         responses={200: CredentialsSerializer,
                                    204: 'No module with your ID',
                                    400: 'No source module with your ID'})
    def get(self, request, id):
        module_type = 'source'
        return get_credentials(module_type, id)

    @swagger_auto_schema(operation_description='Set credentials',
                         request_body=CredentialsSerializer,
                         responses={200: CredentialsSerializer,
                                    204: 'No module with your ID',
                                    400: 'No source module with your ID'})
    def post(self, request, id):
        module_type = 'source'
        return Response(set_credentials(module_type, id, request.data['credentials']))


class GetParserValidateStatusAPI(APIView):
    @swagger_auto_schema(operation_description='get where: validate what: status',
                         responses={200: 'String',
                                    204: 'No data',
                                    400: 'No module name',
                                    405: 'Url is incorrect'})
    def get(self, request, gen_id_or_cur_gen, pk, module_name):
        return get_info(pk,  get_generation_number(pk,gen_id_or_cur_gen), 'parser', module_name,
                        'Validate', 'status')


class GetParserValidateErrorsAPI(APIView):
    @swagger_auto_schema(operation_description='get where: validate what: errors',
                         responses={200: 'String',
                                    204: 'No data',
                                    400: 'No module name',
                                    405: 'Url is incorrect'})
    def get(self, request, gen_id_or_cur_gen, pk, module_name):
        return get_info(pk,  get_generation_number(pk,gen_id_or_cur_gen), 'parser', module_name,
                        'Validate', 'errors')


class GetParserStopFactorStatusAPI(APIView):
    @swagger_auto_schema(operation_description='get where: stopfactor what: status',
                         responses={200: 'String',
                                    204: 'No data',
                                    400: 'No module name',
                                    405: 'Url is incorrect'})
    def get(self, request, gen_id_or_cur_gen, pk, module_name):
        return get_info(pk,  get_generation_number(pk,gen_id_or_cur_gen), 'parser', module_name,
                        'StopFactors', 'status')


class GetParserStopFactorErrorsAPI(APIView):
    @swagger_auto_schema(operation_description='get where: stopfactor what: errors',
                         responses={200: 'String',
                                    204: 'No data',
                                    400: 'No module name',
                                    405: 'Url is incorrect'})
    def get(self, request, gen_id_or_cur_gen, pk, module_name):
        return get_info(pk,  get_generation_number(pk,gen_id_or_cur_gen), 'parser', module_name,
                        'StopFactors', 'errors')


class GetParserValuesAPI(APIView):
    @swagger_auto_schema(operation_description='get_values',
                         responses={200: 'String',
                                    204: 'No data',
                                    400: 'No module name'})
    def get(self, request, gen_id_or_cur_gen, pk, module_name):
        return get_info(pk,  get_generation_number(pk,gen_id_or_cur_gen), 'parser', module_name, 'Values')


class GetAllParserValuesAPI(APIView):
    @swagger_auto_schema(operation_description='get_all_values',
                        responses={200: 'Array'})
    def get(self, request, pk, gen_id_or_cur_gen):
        return get_list_info(pk, get_generation_number(pk,gen_id_or_cur_gen), 'parser', 'Values')


class GetParserValidateAllErrorsAPI(APIView):
    @swagger_auto_schema(operation_description='get_all_errors validate',
                         responses={200: 'Array'})
    def get(self, request, gen_id_or_cur_gen, pk):
        return get_list_info(pk, get_generation_number(pk, gen_id_or_cur_gen), 'parser', 'Validate', 'errors')


class GetParserStopFactorAllErrorsAPI(APIView):
    @swagger_auto_schema(operation_description='get_all_errors stopfactor',
                         responses={200: 'Array'})
    def get(self, request, gen_id_or_cur_gen, pk):
        return get_list_info(pk, get_generation_number(pk, gen_id_or_cur_gen), 'parser', 'StopFactors', 'errors')


class GetParserValidateAllStatusAPI(APIView):
    @swagger_auto_schema(operation_description='get_all_errors validate',
                         responses={200: 'Array'})
    def get(self, request, gen_id_or_cur_gen, pk):
        return get_list_info(pk, get_generation_number(pk, gen_id_or_cur_gen), 'parser', 'Validate', 'status')


class GetParserStopFactorAllStatusAPI(APIView):
    @swagger_auto_schema(operation_description='get_all_errors stopfactor',
                         responses={200: 'Array'})
    def get(self, request, gen_id_or_cur_gen, pk):
        return get_list_info(pk, get_generation_number(pk, gen_id_or_cur_gen), 'parser', 'StopFactors', 'status')


class GetScoringAPI(APIView):
    @swagger_auto_schema(operation_description='get_score',
                         responses={200: 'String',
                                    204: 'No data',
                                    400: 'No module name'})
    def get(self, request, gen_id_or_cur_gen, pk, module_name):
        return get_info(pk,  get_generation_number(pk,gen_id_or_cur_gen), 'scoring', module_name, 'Score')


class GetAllScoringAPI(APIView):
    @swagger_auto_schema(operation_description='get all score',
                         responses={200: 'Array',
                                    204: 'No data'})
    def get(self, request, gen_id_or_cur_gen, pk):
        return get_all_info(pk,  get_generation_number(pk,gen_id_or_cur_gen), 'scoring', 'Score')

