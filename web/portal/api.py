import json
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from web.portal.models import *
from web.portal.serializers import *

from django.forms.models import model_to_dict


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer

class create_raw_client(APIView):
    #оставляем старое?
    def get(self,request):
        #     try:
        #         new_client = Client()
        #
        #         body_unicode = request.body.decode('utf-8')
        #         json_data = json.loads(body_unicode)
        #
        #         new_client.client_id = json_data['id']
        #         new_client.client_type_id = json_data['client_type_id']
        #         new_client.client_type = json_data['client_type']
        #         new_client.communication_id = json_data['communication_id']
        #         new_client.communication = json_data['communication']
        #         new_client.phone_confirm = json_data['phone_confirm']
        #         new_client.welcome = json_data['welcome']
        #         new_client.amocrm_deal_id = json_data['amocrm_deal_id']
        #         new_client.ga_client_id = json_data['ga_client_id']
        #         new_client.utm_source = json_data['utm_source']
        #         new_client.utm_medium = json_data['utm_medium']
        #         new_client.created_at = json_data['created_at']
        #         new_client.main_driver_id = json_data['driver_id']
        #         #        new_client.save()
        #
        #         new_drivers = []
        #         new_passports = []
        #         new_images_passport = []
        #         new_images_license = []
        #         new_licenses = []
        #
        #         for drvr in range(0, len(json_data['drivers'])):
        #             new_driver = Driver()
        #             json_driver = json_data['drivers'][drvr]
        #
        #             new_driver.client = new_client
        #             new_driver.driver_id = json_driver['id']
        #             new_driver.lastname = json_driver['lastname']
        #             new_driver.firstname = json_driver['firstname']
        #             new_driver.middlename = json_driver['middlename']
        #             new_driver.email = json_driver['email']
        #             new_driver.phone = json_driver['phone']
        #             new_driver.gender_id = json_driver['gender_id']
        #             new_driver.gender = json_driver['gender']
        #             new_driver.birthday = json_driver['birthday']
        #             #            new_driver.save(
        #             new_drivers.append(new_driver)
        #
        #             new_passport = Passport()
        #             json_driver_pass = json_driver['passport']
        #
        #             new_passport.driver = new_driver
        #             new_passport.number = json_driver_pass['number']
        #             new_passport.issued_at = json_driver_pass['issued_at']
        #             new_passport.issued_by = json_driver_pass['issued_by']
        #             new_passport.address_registration = json_driver_pass['address_registration']
        #             new_passport.division_code = json_driver_pass['division_code']
        #             new_passport.birthplace = json_driver_pass['birthplace']
        #             new_passport.created_at = json_driver_pass['created_at']
        #             # new_passport.save()
        #             new_passports.append(new_passport)
        #
        #             for img in range(1, 5):
        #                 new_img = Image()
        #                 new_img.passport = new_passport
        #                 new_img_txt = 'image{0}'.format(img)
        #
        #                 new_img.title = json_driver_pass[new_img_txt]
        #                 new_img.confirm_id = json_driver_pass[new_img_txt + '_confirm_id']
        #                 new_img.confirm = json_driver_pass[new_img_txt + '_confirm']
        #                 new_img.url = json_driver_pass[new_img_txt + '_url']
        #                 # new_img.save()
        #                 new_images_passport.append(new_img)
        #
        #             new_license = License()
        #             json_driver_lcn = json_driver['driver_license']
        #
        #             new_license.driver = new_driver
        #             new_license.number = json_driver_lcn['number']
        #             new_license.issued_at = json_driver_lcn['issued_at']
        #             new_license.finished_at = json_driver_lcn['finished_at']
        #             new_license.created_at = json_driver_lcn['created_at']
        #             # new_license.save()
        #             new_licenses.append(new_license)
        #
        #             for img in range(1, 3):
        #                 new_img = Image()
        #                 new_img.license = new_license
        #                 new_img_txt = 'image{0}'.format(img)
        #
        #                 new_img.title = json_driver_lcn[new_img_txt]
        #                 new_img.confirm_id = json_driver_lcn[new_img_txt + '_confirm_id']
        #                 new_img.confirm = json_driver_lcn[new_img_txt + '_confirm']
        #                 new_img.url = json_driver_lcn[new_img_txt + '_url']
        #                 # new_img.save()
        #                 new_licenses.append(new_img)
        #
        #         new_client.save()
        #         for driver in new_drivers:
        #             driver.client = new_client
        #             driver.save()
        #             for passport in new_passports:
        #                 passport.driver = driver
        #                 passport.save()
        #                 for image in new_images_passport:
        #                     image.passport = passport
        #                     image.save()
        #             for dlicense in new_licenses:
        #                 dlicense.driver = driver
        #                 dlicense.save()
        #                 for image in new_images_license:
        #                     image.license = dlicense
        #                     image.save()
        #
        #     except KeyError as e:
        #         return JsonResponse({'Status': 'ERROR', 'Exception': 'No key: {0}'.format(e)})
        #
        #     except Exception as e:
        #         return JsonResponse({'Status': 'ERROR', 'Exception': 'Server error: {0}'.format(e)})
        #
        #     else:
        #         return JsonResponse({'Status': 'OK'})
        return Response(status=status.HTTP_200_OK)


class start_task(APIView):
    def get(self,request):
        #дописать
        return Response(status=status.HTTP_200_OK)


class finalize_task(APIView):
    def get(self,request):
        task_id = self.request.query_params.get('task_id', None)
        if task_id is not None:
            #не пойму какую таблицу юзать
            task_table = HZ.objects.filter(task=task_id)
            task_table.task_status =2
            task_table.save
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class create_passport(APIView):
    def get(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def post(self,request):
        serializer = PassportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class create_license(APIView):
    def get(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def post(self,request):
        serializer = LicenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class create_individual(APIView):
    def get(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def post(self,request):
        serializer = IndividualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class create_image(APIView):
    def get(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def post(self,request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class create_client(APIView):
    def get(self,request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def post(self,request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class update_client_task_data(APIView):
    def get(self,request):
        task_id = self.request.query_params.get('task_id', None)
        client_id = self.request.query_params.get('client_id', None)

        if task_id and client_id is not None:
            task_table = ClientTask.objects.filter(task=task_id)
            task_table.client = client_id
            task_table.save
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class get_default_score_model(APIView):
    def get(self,request):
        return JsonResponse({'score_model id': '1'})


class get_sources(APIView):
    def get(self,request):
        return Response(status=status.HTTP_200_OK)


class get_individual_passport(APIView):
    def get(self,request):
        queryset = PassportSerializer.objects.all()
        individual_id = self.request.query_params.get('individual_id', None)
        if individual_id is not None:
            queryset = queryset.filter(individual_id=individual_id)
            return queryset
        return Response(status=status.HTTP_400_BAD_REQUEST)


class get_individual_license(APIView):
    def get(self,request):
        queryset = LicenseSerializer.objects.all()
        individual_id = self.request.query_params.get('individual_id', None)
        if individual_id is not None:
            queryset = queryset.filter(individual_id=individual_id)
            return queryset
        return Response(status=status.HTTP_400_BAD_REQUEST)


class create_source_raw_data(APIView):
    def get(self,request):
        return Response(status=status.HTTP_200_OK)


class update_source_task(APIView):
    def get(self,request):
        return Response(status=status.HTTP_200_OK)


class get_source_raw_data_for_individual(APIView):
    def get(self,request):
        return Response(status=status.HTTP_200_OK)


class insert_check(APIView):
    def get(self,request):
        individual_id = self.request.query_params.get('individual_id', None)
        value = self.request.query_params.get('value', None)
        check_registry_id = self.request.query_params.get('check_registry_id', None)

        if individual_id and value and check_registry_id is not None:
            check_table = Check.objects.filter(individual=individual_id,checkRegistry=check_registry_id)
            check_table.value = value
            check_table.save
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

