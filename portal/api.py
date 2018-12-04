from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.shortcuts import redirect
from portal.models import *
import datetime
import pytz


def api_create(request):
    if request.method == "POST":
        try:
            new_client = Client()

            body_unicode = request.body.decode('utf-8')
            json_data = json.loads(body_unicode)

            new_client.client_id = json_data['id']
            new_client.client_type_id = json_data['client_type_id']
            new_client.client_type = json_data['client_type']
            new_client.communication_id = json_data['communication_id']
            new_client.communication = json_data['communication']
            new_client.phone_confirm = json_data['phone_confirm']
            new_client.welcome = json_data['welcome']
            new_client.amocrm_deal_id = json_data['amocrm_deal_id']
            new_client.ga_client_id = json_data['ga_client_id']
            new_client.utm_source = json_data['utm_source']
            new_client.utm_medium = json_data['utm_medium']
            new_client.created_at = json_data['created_at']
            new_client.main_driver_id = json_data['driver_id']
            #        new_client.save()

            new_drivers = []
            new_passports = []
            new_images_passport = []
            new_images_license = []
            new_licenses = []

            for drvr in range(0, len(json_data['drivers'])):
                new_driver = Driver()
                json_driver = json_data['drivers'][drvr]

                new_driver.client = new_client
                new_driver.driver_id = json_driver['id']
                new_driver.lastname = json_driver['lastname']
                new_driver.firstname = json_driver['firstname']
                new_driver.middlename = json_driver['middlename']
                new_driver.email = json_driver['email']
                new_driver.phone = json_driver['phone']
                new_driver.gender_id = json_driver['gender_id']
                new_driver.gender = json_driver['gender']
                new_driver.birthday = json_driver['birthday']
                #            new_driver.save(
                new_drivers.append(new_driver)

                new_passport = Passport()
                json_driver_pass = json_driver['passport']

                new_passport.driver = new_driver
                new_passport.number = json_driver_pass['number']
                new_passport.issued_at = json_driver_pass['issued_at']
                new_passport.issued_by = json_driver_pass['issued_by']
                new_passport.address_registration = json_driver_pass['address_registration']
                new_passport.division_code = json_driver_pass['division_code']
                new_passport.birthplace = json_driver_pass['birthplace']
                new_passport.created_at = json_driver_pass['created_at']
                # new_passport.save()
                new_passports.append(new_passport)

                for img in range(1, 5):
                    new_img = Image()
                    new_img.passport = new_passport
                    new_img_txt = 'image{0}'.format(img)

                    new_img.title = json_driver_pass[new_img_txt]
                    new_img.confirm_id = json_driver_pass[new_img_txt + '_confirm_id']
                    new_img.confirm = json_driver_pass[new_img_txt + '_confirm']
                    new_img.url = json_driver_pass[new_img_txt + '_url']
                    # new_img.save()
                    new_images_passport.append(new_img)

                new_license = License()
                json_driver_lcn = json_driver['driver_license']

                new_license.driver = new_driver
                new_license.number = json_driver_lcn['number']
                new_license.issued_at = json_driver_lcn['issued_at']
                new_license.finished_at = json_driver_lcn['finished_at']
                new_license.created_at = json_driver_lcn['created_at']
                # new_license.save()
                new_licenses.append(new_license)

                for img in range(1, 3):
                    new_img = Image()
                    new_img.license = new_license
                    new_img_txt = 'image{0}'.format(img)

                    new_img.title = json_driver_lcn[new_img_txt]
                    new_img.confirm_id = json_driver_lcn[new_img_txt + '_confirm_id']
                    new_img.confirm = json_driver_lcn[new_img_txt + '_confirm']
                    new_img.url = json_driver_lcn[new_img_txt + '_url']
                    # new_img.save()
                    new_licenses.append(new_img)

            new_client.save()
            for driver in new_drivers:
                driver.client = new_client
                driver.save()
                for passport in new_passports:
                    passport.driver = driver
                    passport.save()
                    for image in new_images_passport:
                        image.passport = passport
                        image.save()
                for dlicense in new_licenses:
                    dlicense.driver = driver
                    dlicense.save()
                    for image in new_images_license:
                        image.license = dlicense
                        image.save()

        except KeyError as e:
            return JsonResponse({'Status': 'ERROR', 'Exception': 'No key: {0}'.format(e)})

        except Exception as e:
            return JsonResponse({'Status': 'ERROR', 'Exception': 'Server error: {0}'.format(e)})

        else:
            return JsonResponse({'Status': 'OK'})

    else:
        return JsonResponse({'Status': 'WAITING'})
