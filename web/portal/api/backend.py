from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.views import APIView
from drf_yasg import openapi
import json
from core.lib import message_sender, api_requestor
from portal.lib.backend_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from web.portal.serializers.backend import *
from web.portal.models import *

from rest_framework import viewsets


class GenerationApi(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Generation.objects.all()
    serializer_class = GenerationSerializer


class ClientApi(mixins.ListModelMixin,mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientGetSerializer


class CreateClientApi(mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

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


class RawClientDataApi(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = RawClientData.objects.all()
    serializer_class = RawClientDataSerializer



class NewActionApi(APIView):
    @swagger_auto_schema(operation_description='Create new action',
                         request_body=NewActionSerializer)
    def post(self, request):
        raw_data = request.data
        generation = Generation.objects.get(individual_id=raw_data['individual'])
        action = Action.objects.create(generation=generation, processor=raw_data['processor'],
                                           action_type=raw_data['action_type'],
                                           payload=raw_data['payload'],
                                           create_time=datetime.datetime.now())
        action.save()
        return Response(status=status.HTTP_201_CREATED)


class BusMessageAPI(APIView):
    @swagger_auto_schema(operation_description='Send message to message bus',
                         request_body=BusMessageSerializer)
    def post(self, request):
        raw_data = request.data
        serializer = BusMessageSerializer(data=raw_data)
        if serializer.is_valid():
            message_sender.send_message(message_code=serializer.validated_data['message_type'],
                                        body=serializer.validated_data['body'])
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class WillzCreateClient(APIView):
    @swagger_auto_schema(operation_description='Create new Willz client from raw_data',
                         request_body=openapi.Schema(type=openapi.TYPE_STRING, description='Raw JSON from Willz'))
    def post(self, request):
        raw_json = json.dumps(request.data)
        my_json = {"payload": raw_json}
        serializer = RawClientDataSerializer(data=my_json)

        if serializer.is_valid():
            resp_data = serializer.save()
            resp = json.dumps({'message_type': constants.CLIENT_RAW_CREATED_MESSAGE,
                               'body': json.dumps({'raw_client_id': resp_data.id})});

            raw_data = api_requestor.post('/back/bus_message/', resp)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# *** PARSER METHODS ***
class ParserGetAPI(APIView):
    @swagger_auto_schema(operation_description='Get current module',
                        responses={200: ParserGetModuleSerializer,
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, get_module_by_id_type, module_type=ParserModule)


class ParserActivateAPI(APIView):
    @swagger_auto_schema(operation_description='Activate current module',
                        responses={200: 'Activated',
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, set_module_is_active_by_id_type, is_active=True,
                                  module_type=ParserModule)


class ParserDeactivateAPI(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module',
                        responses={200: 'Deactivated',
                                204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, set_module_is_active_by_id_type, is_active=False,
                                  module_type=ParserModule)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class ParserGetParametersAPI(APIView):
    @swagger_auto_schema(operation_description='Get parameters',
                        responses={200: 'Parameters',
                                    204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, get_module_parameters, module_type=ParserModule)


# *** SCORING METHODS ***
class ScoringGetAPI(APIView):
    @swagger_auto_schema(operation_description='Get current module',
                        responses={200: ScoringGetModuleSerializer,
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, get_module_by_id_type, module_type=ScoringModule)

class ScoringActivateAPI(APIView):
    @swagger_auto_schema(operation_description='Activate current module',
                        responses={200: 'Activated',
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, set_module_is_active_by_id_type, is_active=True,
                                  module_type=ScoringModule)

class ScoringDeactivateAPI(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module',
                        responses={200: 'Deactivated',
                                204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, set_module_is_active_by_id_type, is_active=False,
                                  module_type=ScoringModule)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class ScoringGetParametersAPI(APIView):
    @swagger_auto_schema(operation_description='Get parameters',
                        responses={200: 'Parameters',
                                    204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, get_module_parameters, module_type=ScoringModule)



# *** SOURCE METHODS ***
class SourceGetAPI(APIView):
    @swagger_auto_schema(operation_description='Get current module',
                        responses={200: SourceGetModuleSerializer,
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, get_module_by_id_type, module_type=SourceModule)


class SourceActivateAPI(APIView):
    @swagger_auto_schema(operation_description='Activate current module',
                        responses={200: 'Activated',
                                   204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, set_module_is_active_by_id_type, is_active=True,
                                  module_type=SourceModule)


class SourceDeactivateAPI(APIView):
    @swagger_auto_schema(operation_description='Deactivate current module',
                        responses={200: 'Deactivated',
                                204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, set_module_is_active_by_id_type, is_active=False,
                                  module_type=SourceModule)


# TODO: Не было тестирования этой части(с настоящими файлами!)
class SourceGetParametersAPI(APIView):
    @swagger_auto_schema(operation_description='Get parameters',
                        responses={200: 'Parameters',
                                    204: 'No module with such PK'})
    def get(self, request, pk):
        return standard_get_by_pk(request, pk, get_module_parameters, module_type=SourceModule)
