from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins

from web.portal.serializers import *

from rest_framework import views, viewsets


class ClientApi(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class IndividualsApi(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer


class ScoringModelsApi(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ScoreModel.objects.all()
    serializer_class = ScoreModelSerializer


class TasksModelApi(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
#
# class start_task(APIView):
#     def get(self,request):
#         #дописать
#         return Response(status=status.HTTP_200_OK)
#
#
# class finalize_task(APIView):
#     def get(self,request):
#         task_id = self.request.query_params.get('task_id', None)
#         if task_id is not None:
#             #не пойму какую таблицу юзать
#             task_table = Task.objects.filter(task=task_id)
#             task_table.task_status =2
#             task_table.save
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
# class create_passport(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = PassportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_license(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = LicenseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_individual(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = IndividualSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_image(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_client(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     def post(self,request):
#         serializer = ClientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class update_client_task_data(APIView):
#     def get(self,request):
#         task_id = self.request.query_params.get('task_id', None)
#         client_id = self.request.query_params.get('client_id', None)
#
#         if task_id and client_id is not None:
#             task_table = ClientTask.objects.filter(task=task_id)
#             task_table.client = client_id
#             task_table.save
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
# class get_default_score_model(APIView):
#     def get(self,request):
#         return JsonResponse({'score_model id': '1'})
#
#
# class get_sources(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class get_individual_passport(APIView):
#     def get(self,request):
#         queryset = PassportSerializer.objects.all()
#         individual_id = self.request.query_params.get('individual_id', None)
#         if individual_id is not None:
#             queryset = queryset.filter(individual_id=individual_id)
#             return queryset
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# class get_individual_license(APIView):
#     def get(self,request):
#         queryset = LicenseSerializer.objects.all()
#         individual_id = self.request.query_params.get('individual_id', None)
#         if individual_id is not None:
#             queryset = queryset.filter(individual_id=individual_id)
#             return queryset
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# class create_source_raw_data(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class update_source_task(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class get_source_raw_data_for_individual(APIView):
#     def get(self,request):
#         return Response(status=status.HTTP_200_OK)
#
#
# class insert_check(APIView):
#     def get(self,request):
#         individual_id = self.request.query_params.get('individual_id', None)
#         value = self.request.query_params.get('value', None)
#         check_registry_id = self.request.query_params.get('check_registry_id', None)
#
#         if individual_id and value and check_registry_id is not None:
#             check_table = Check.objects.filter(individual=individual_id,checkRegistry=check_registry_id)
#             check_table.value = value
#             check_table.save
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
