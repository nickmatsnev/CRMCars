from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from portal.lib.frontend_api_helpers import save_module, standard_post, standard_get_list, \
    get_modules, get_all_parameters_from_active_modules
from core.lib.modules import SourceModule, ScoringModule, ParserModule

from web.portal.serializers.frontend import *
from web.portal.serializers.backend import *
from web.portal.models import *

from django.contrib.auth.models import User
from rest_framework.parsers import FormParser,MultiPartParser


from core.lib import constants
from rest_framework import viewsets
from core.lib import api_requestor


class UserListApi(mixins.ListModelMixin, mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClientsListApi(APIView):

    @swagger_auto_schema(operation_description='GET /front/clients/')
    def get(self, request):
        items = []
        clients = Client.objects.all()
        serializer = ClientGetSerializer(clients, many=True)
        cntr = 0
        for client in serializer.data:
            for individual in client['individuals']:
                if individual['primary'] == True:
                    new_item = {}
                    new_item['fio'] = individual['first_name'] + ' ' + individual['last_name']
                    cntr += 1
                    new_item['num'] = cntr
                    new_item['id'] = client['id']
                    new_item['created_at'] = client['created_at']
                    new_item['status'] = get_status(individual['id'])

                    items.append(new_item)
        return Response(items)


class ClientInspectApi(APIView):

    @swagger_auto_schema(operation_description='GET /front/clients/<int:id>/')
    def get(self, request, pk):
        queryset = Client.objects.get(id=pk)
        serializer = ClientGetSerializer(queryset, many=False)

        individual = {}
        drivers = []
        for individual_raw in serializer.data['individuals']:
            driver ={}
            driver['name']=individual_raw['first_name']
            driver['surname'] = individual_raw['last_name']
            driver['number'] = individual_raw['driver_license']['number']
            driver['issued_at'] = individual_raw['driver_license']['issued_at']
            driver['primary'] = individual_raw['primary']
            if individual_raw['primary'] == True:
                individual = individual_raw

            drivers.append(driver)

        op_history = []
        queryset = Generation.objects.get(individual_id=individual['id'])
        serializer = GenerationSerializer(queryset, many=False)
        op_history = serializer.data

        items = {}
        items['id'] = pk
        items['individual'] = individual
        items['drivers'] = drivers
        items['op_history'] = op_history

        return Response(items)


def get_status(individual_id):
    gen_data = api_requestor.request('/back/generation/{0}'.format(individual_id))
    source_cnt = 0
    check_cnt = 0
    scorint_cnt = 0
    declined = False
    accepted = False
    new = False

    for act in gen_data['actions']:
        if act['action_type'] == 'declined':
            declined =  True
        if act['action_type'] == 'accepted':
            accepted = True
        if act['action_type'] == 'new':
            new = True


    # определить что выше по приоритетам!
    if declined==True:
        return 'Отказано'
    if accepted==True:
        return 'Одобрено'

    if new == True:
        return 'Новый'

    return 'Неизвестно'


class ParserGetParametersFromActiveModules(APIView):
    @swagger_auto_schema(operation_description='Get active parameters',
                        responses={200: 'Table: source,parser,name,description,type'})
    def get(self, request):
        return standard_get_list(request, get_all_parameters_from_active_modules, module_type=ParserModule)


class ParserGetAllAPI(APIView):
    @swagger_auto_schema(operation_description='Get all parsers',
                            responses={200: 'Table: name,path,is_active,creation_time'})
    def get(self, request):
        return standard_get_list(request, get_modules, module_type=ParserModule)



class ParserUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    #@swagger_auto_schema(operation_description='Parser upload API',
     #                    request_body=openapi.Schema(type=openapi.TYPE_STRING, description='.py file'))
    def post(self, request):
        return standard_post(request, save_module, serializer=ParserModuleSerializer,
                             path_to_modules=constants.PATH_TO_PARSER_MODULES)



class ScoringGetAllAPI(APIView):
    @swagger_auto_schema(operation_description='Get all scorings',
                            responses={200: 'Table: name,path,is_active,creation_time'})
    def get(self, request):
        return standard_get_list(request, get_modules, module_type=ScoringModule)


class ScoringUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    #@swagger_auto_schema(operation_description='Parser upload API',
     #                    request_body=openapi.Schema(type=openapi.TYPE_STRING, description='.py file'))

    def post(self, request):
        def post(self, request):
            return standard_post(request, save_module, serializer=ScoringModuleSerializer,
                                 path_to_modules=constants.PATH_TO_SCORING_MODULES)


class SourceGetAllAPI(APIView):
    @swagger_auto_schema(operation_description='Get all sources',
                            responses={200: 'Table: name,path,is_active,creation_time,credentials'})
    def get(self, request):
        return standard_get_list(request, get_modules, module_type=SourceModule)


class SourceUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    #@swagger_auto_schema(operation_description='Parser upload API',
     #                    request_body=openapi.Schema(type=openapi.TYPE_STRING, description='.py file'))

    def post(self, request):
        return standard_post(request, save_module, serializer=SourceModuleSerializer,
                             path_to_modules=constants.PATH_TO_SOURCE_MODULES)
