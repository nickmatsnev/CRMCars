import xlrd
import json
import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')

from core.lib.global_settings import *
from core.lib.api import ApiRequestor
from core.lib.datetime_converters import *


# Номера столбцов
COL_ID = 1
COL_PHONE = 48
COL_CLIENT_TYPE_ID = 4
#COL_CLIENT_TYPE = 0
COL_LASTNAME = 10
COL_FIRSTNAME = 9
COL_MIDDLENAME = 11
COL_EMAIL = 12
#COL_GENDER_ID = 0
COL_GENDER = 13
COL_BIRTHDAY = 14
#COL_COMMUNICATION_ID = 0
COL_COMMUNICATION = 15
COL_PHONE_CONFIRM = 16
COL_WELCOME = 17
COL_AMORCRM_DEAL_ID = 19
#COL_GA_CLIENT_ID = 0
COL_UTM_SOURCE = 21
COL_UTM_MEDIUM = 22
COL_CREATED_AT = 23
COL_PASSPORT_DRIVER_ID = 5
COL_PASSPORT_IMAGE1_URL = 26
COL_PASSPORT_IMAGE1_CONFIRM = 25
COL_PASSPORT_IMAGE2_URL = 28
COL_PASSPORT_IMAGE2_CONFIRM = 27
COL_PASSPORT_IMAGE3_URL = 30
COL_PASSPORT_IMAGE3_CONFIRM = 29
COL_PASSPORT_IMAGE4_URL = 32
COL_PASSPORT_IMAGE4_CONFIRM = 31
COL_PASSPORT_NUMBER = 33
COL_PASSPORT_ISSUED_AT = 34
COL_PASSPORT_ISSUED_BY = 35
COL_PASSPORT_ADDRESS_REGISTRATION = 36
COL_PASSPORT_DIVISION_CODE = 37
COL_PASSPORT_BIRTHPLACE = 38
COL_PASSPORT_CREATED_AT = 39
COL_DRIVER_ID = 6



COL_DRIVER_LICENSE_ID = 52
COL_DRIVER_LICENSE_IMAGE1_CONFIRM = 53
COL_DRIVER_LICENSE_IMAGE1_URL = 54
COL_DRIVER_LICENSE_IMAGE2_CONFIRM = 55
COL_DRIVER_LICENSE_IMAGE2_URL = 56
COL_DRIVER_LICENSE_NUMBER = 58
COL_DRIVER_LICENSE_ISSUED_AT = 59
#COL_DRIVER_LICENSE_FINISHED_AT= 0
COL_DRIVER_LICENSE_CREATED_AT= 60


def do_import(limit=0):
    rb = xlrd.open_workbook(EXCEL_TO_READ_PATH)
    sheet = rb.sheet_by_index(0)
    index = 0
    for rownum in range(1, sheet.nrows):
        if limit != 0 and index == limit:
            break
        row = sheet.row_values(rownum)
        willz_client = {}
        willz_client['id'] = int(row[COL_ID - 1])
        willz_client['phone'] = row[COL_PHONE - 1]
        willz_client['client_type_id'] = int(row[COL_CLIENT_TYPE_ID - 1])
        willz_client['client_type'] = 'Физ. лицо'
        willz_client['lastname'] = row[COL_LASTNAME - 1]
        willz_client['firstname'] = row[COL_FIRSTNAME - 1]
        willz_client['middlename'] = row[COL_MIDDLENAME - 1]
        willz_client['email'] = row[COL_EMAIL - 1]
        gender = int(row[COL_GENDER - 1]) if row[COL_GENDER - 1] != '' else 0
        willz_client['gender_id'] = gender
        willz_client['gender'] = gender
        willz_client['birthday'] = row[COL_BIRTHDAY - 1]
        willz_client['communication'] = str(row[COL_COMMUNICATION - 1])
        willz_client['phone_confirm'] = str(row[COL_PHONE_CONFIRM - 1])
        willz_client['welcome'] = int(row[COL_WELCOME - 1])
        willz_client['amocrm_deal_id'] = int(row[COL_AMORCRM_DEAL_ID - 1])
        willz_client['ga_client_id'] = ''
        willz_client['utm_source'] = row[COL_UTM_SOURCE - 1]
        willz_client['utm_medium'] = row[COL_UTM_MEDIUM - 1]
        willz_client['created_at'] = datetime_converter(row[COL_CREATED_AT - 1])

        my_passport = {}
        my_passport['id'] = int(row[COL_PASSPORT_DRIVER_ID - 1])
        my_passport['image1'] = "Первый разворот"
        my_passport['image1_confirm_id'] = ""
        my_passport['image1_confirm'] = str(row[COL_PASSPORT_IMAGE1_CONFIRM - 1])
        my_passport['image1_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE1_URL - 1]
        my_passport['image2'] = "Разворот с регистрацией"
        my_passport['image2_confirm_id'] = ""
        my_passport['image2_confirm'] = str(row[COL_PASSPORT_IMAGE2_CONFIRM - 1])
        my_passport['image2_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE2_URL - 1]
        my_passport['image3'] = "Селфи с паспортом"
        my_passport['image3_confirm_id'] = ""
        my_passport['image3_confirm'] = str(row[COL_PASSPORT_IMAGE3_CONFIRM - 1])
        my_passport['image3_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE3_URL - 1]
        my_passport['image4'] = "Подтверждение дохода"
        my_passport['image4_confirm_id'] = ""
        my_passport['image4_confirm'] = str(row[COL_PASSPORT_IMAGE4_CONFIRM - 1])
        my_passport['image4_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE4_URL - 1]
        my_passport['number'] = row[COL_PASSPORT_NUMBER - 1]
        my_passport['issued_at'] = row[COL_PASSPORT_ISSUED_AT - 1]
        my_passport['issued_by'] = row[COL_PASSPORT_ISSUED_BY - 1]
        my_passport['address_registration'] = row[COL_PASSPORT_ADDRESS_REGISTRATION - 1]
        my_passport['division_code'] = row[COL_PASSPORT_DIVISION_CODE - 1]
        my_passport['birthplace'] = row[COL_PASSPORT_BIRTHPLACE - 1]
        my_passport['created_at'] = date_converter(row[COL_DRIVER_LICENSE_CREATED_AT - 1])
        willz_client['passport'] = my_passport

        willz_client['driver_id'] = int(row[COL_DRIVER_ID - 1])

        drivers = []
        driver = {}
        driver['id'] = int(row[COL_DRIVER_ID - 1])
        driver['lastname'] = row[COL_LASTNAME - 1]
        driver['firstname'] = row[COL_FIRSTNAME - 1]
        driver['middlename'] = row[COL_MIDDLENAME - 1]
        driver['email'] = row[COL_EMAIL - 1]
        driver['phone'] = row[COL_PHONE - 1]
        driver['gender_id'] = gender
        driver['gender'] = gender
        driver['birthday'] = row[COL_BIRTHDAY - 1]

        my_passport = {}
        my_passport['id'] = int(row[COL_PASSPORT_DRIVER_ID - 1])
        my_passport['image1'] = "Первый разворот"
        my_passport['image1_confirm_id'] = ""
        my_passport['image1_confirm'] = row[COL_PASSPORT_IMAGE1_CONFIRM - 1]
        my_passport['image1_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE1_URL - 1]
        my_passport['image2'] = "Разворот с регистрацией"
        my_passport['image2_confirm_id'] = ""
        my_passport['image2_confirm'] = row[COL_PASSPORT_IMAGE2_CONFIRM - 1]
        my_passport['image2_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE2_URL - 1]
        my_passport['image3'] = "Селфи с паспортом"
        my_passport['image3_confirm_id'] = ""
        my_passport['image3_confirm'] = row[COL_PASSPORT_IMAGE3_CONFIRM - 1]
        my_passport['image3_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE3_URL - 1]
        my_passport['image4'] = "Подтверждение дохода"
        my_passport['image4_confirm_id'] = ""
        my_passport['image4_confirm'] = row[COL_PASSPORT_IMAGE4_CONFIRM - 1]
        my_passport['image4_url'] = EXCEL_TO_READ_PASSPORT_PATH + row[COL_PASSPORT_IMAGE4_URL - 1]
        my_passport['number'] = str(row[COL_PASSPORT_NUMBER - 1]).replace(" ", "")
        my_passport['issued_at'] = date_converter(row[COL_PASSPORT_ISSUED_AT - 1])
        my_passport['issued_by'] = row[COL_PASSPORT_ISSUED_BY - 1]
        my_passport['address_registration'] = row[COL_PASSPORT_ADDRESS_REGISTRATION - 1]
        my_passport['division_code'] = row[COL_PASSPORT_DIVISION_CODE - 1]
        my_passport['birthplace'] = row[COL_PASSPORT_BIRTHPLACE - 1]
        my_passport['created_at'] = date_converter(row[COL_DRIVER_LICENSE_CREATED_AT - 1])
        driver['passport'] = my_passport

        driver_license = {}
        driver_license['id'] = int(row[COL_DRIVER_LICENSE_ID - 1])
        driver_license['image1'] = "Фото передней стороны"
        driver_license['image1_confirm_id'] = ""
        driver_license['image1_confirm'] = row[COL_DRIVER_LICENSE_IMAGE1_CONFIRM - 1]
        driver_license['image1_url'] = EXCEL_TO_READ_DRIVER_LICENSES_PATH + row[COL_DRIVER_LICENSE_IMAGE1_URL - 1]
        driver_license['image2'] = "Фото задней стороны"
        driver_license['image2_confirm_id'] = ""
        driver_license['image2_confirm'] = row[COL_DRIVER_LICENSE_IMAGE2_CONFIRM - 1]
        driver_license['image2_url'] = EXCEL_TO_READ_DRIVER_LICENSES_PATH + row[COL_DRIVER_LICENSE_IMAGE2_URL - 1]
        driver_license['number'] = str(row[COL_DRIVER_LICENSE_NUMBER - 1]).replace(" ", "")
        driver_license['issued_at'] = row[COL_DRIVER_LICENSE_ISSUED_AT - 1]
        driver_license['finished_at'] = ""
        driver_license['created_at'] = date_converter(row[COL_DRIVER_LICENSE_CREATED_AT - 1])
        driver['driver_license'] = driver_license

        drivers.append(driver)
        willz_client['drivers'] = drivers

        print(json.dumps(willz_client))
        apiRequestor = ApiRequestor()
        response = apiRequestor.post_new_client(json.dumps(willz_client))
        index += 1

# do_import()
