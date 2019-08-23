import xlrd
import json
import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')

from core.lib.global_settings import *
from core.lib.api import ApiRequestor
from core.lib.datetime_converters import *

NEW_EXCEL_PATH = "../test_data/test22.xlsx"


# Номера столбцов

COL_LASTNAME = 1
COL_FIRSTNAME = 2
COL_MIDDLENAME = 3
COL_GENDER = 4
COL_PHONE = 5
COL_BIRTHDAY = 6
COL_PASSPORT_SERIAL = 7
COL_PASSPORT_NUMBER = 8
COL_PASSPORT_ISSUED_BY = 9
COL_PASSPORT_ISSUED_AT = 10
COL_PASSPORT_DIVISION_CODE = 11

COL_PASSPORT_ADDRESS_REGISTRATION = 21


COL_PASSPORT_BIRTHPLACE_REG = 23
COL_PASSPORT_BIRTHPLACE = 24




def do_import(limit=0):
    rb = xlrd.open_workbook(NEW_EXCEL_PATH)
    sheet = rb.sheet_by_index(0)
    index = 0
    for rownum in range(25, sheet.nrows):
        if limit != 0 and index == limit:
            break
        row = sheet.row_values(rownum)
        willz_client = {}
        willz_client['id'] = int(0)
        willz_client['phone'] = row[COL_PHONE - 1]
        willz_client['client_type_id'] = int(0)
        willz_client['client_type'] = 'Физ. лицо'
        willz_client['lastname'] = row[COL_LASTNAME - 1]
        willz_client['firstname'] = row[COL_FIRSTNAME - 1]
        willz_client['middlename'] = row[COL_MIDDLENAME - 1]
        willz_client['email'] = "blank@blank.com"

        if row[COL_GENDER - 1] == 'Женский':
            gender = 2
        else:
            gender = 1
        willz_client['gender_id'] = gender
        willz_client['gender'] = row[COL_GENDER - 1]

        willz_client['birthday'] = date_converter(row[COL_BIRTHDAY - 1])
        willz_client['communication'] = ""
        willz_client['phone_confirm'] = ""
        willz_client['welcome'] = ""
        willz_client['amocrm_deal_id'] = ""
        willz_client['ga_client_id'] = ''
        willz_client['utm_source'] = ""
        willz_client['utm_medium'] = ""
        willz_client['created_at'] = datetime_converter(None)

        my_passport = {}
        my_passport['id'] = int(0)

        my_passport['image1'] = "Первый разворот"
        my_passport['image1_confirm_id'] = ""
        my_passport['image1_confirm'] = ""
        my_passport['image1_url'] = ""
        my_passport['image2'] = "Разворот с регистрацией"
        my_passport['image2_confirm_id'] = ""
        my_passport['image2_confirm'] = ""
        my_passport['image2_url'] = ""
        my_passport['image3'] = "Селфи с паспортом"
        my_passport['image3_confirm_id'] = ""
        my_passport['image3_confirm'] = ""
        my_passport['image3_url'] = ""
        my_passport['image4'] = "Подтверждение дохода"
        my_passport['image4_confirm_id'] = ""
        my_passport['image4_confirm'] = ""
        my_passport['image4_url'] = ""

        my_passport['number'] = row[COL_PASSPORT_NUMBER - 1]
        my_passport['issued_at'] = date_converter(row[COL_PASSPORT_ISSUED_AT - 1])
        my_passport['issued_by'] = row[COL_PASSPORT_ISSUED_BY - 1]
        my_passport['address_registration'] = row[COL_PASSPORT_ADDRESS_REGISTRATION - 1]
        my_passport['division_code'] = row[COL_PASSPORT_DIVISION_CODE - 1]
        my_passport['birthplace'] = row[COL_PASSPORT_BIRTHPLACE - 1]
        my_passport['created_at'] = date_converter(None)
        willz_client['passport'] = my_passport

        willz_client['driver_id'] = int(0)

        drivers = []
        driver = {}
        driver['id'] = int(0)
        driver['lastname'] = row[COL_LASTNAME - 1]
        driver['firstname'] = row[COL_FIRSTNAME - 1]
        driver['middlename'] = row[COL_MIDDLENAME - 1]
        driver['email'] = "blank@blank.com"
        driver['phone'] = row[COL_PHONE - 1]
        driver['gender_id'] = gender
        driver['gender'] = gender
        driver['birthday'] = row[COL_BIRTHDAY - 1]

        my_passport = {}
        my_passport['id'] = int(0)

        my_passport['image1'] = "Первый разворот"
        my_passport['image1_confirm_id'] = ""
        my_passport['image1_confirm'] = ""
        my_passport['image1_url'] = ""
        my_passport['image2'] = "Разворот с регистрацией"
        my_passport['image2_confirm_id'] = ""
        my_passport['image2_confirm'] = ""
        my_passport['image2_url'] = ""
        my_passport['image3'] = "Селфи с паспортом"
        my_passport['image3_confirm_id'] = ""
        my_passport['image3_confirm'] = ""
        my_passport['image3_url'] =""
        my_passport['image4'] = "Подтверждение дохода"
        my_passport['image4_confirm_id'] = ""
        my_passport['image4_confirm'] = ""
        my_passport['image4_url'] = ""

        my_passport['number'] = str(row[COL_PASSPORT_SERIAL - 1]).replace(" ", "") +' '+ str(row[COL_PASSPORT_NUMBER - 1]).replace(" ", "")
        my_passport['issued_at'] = date_converter(row[COL_PASSPORT_ISSUED_AT - 1].replace('/', '.'))
        my_passport['issued_by'] = row[COL_PASSPORT_ISSUED_BY - 1]
        my_passport['address_registration'] = row[COL_PASSPORT_ADDRESS_REGISTRATION - 1]
        my_passport['division_code'] = row[COL_PASSPORT_DIVISION_CODE - 1]

        if row[COL_PASSPORT_BIRTHPLACE_REG-1] != "":
            birthplace = row[COL_PASSPORT_BIRTHPLACE_REG-1] + ', ' + row[COL_PASSPORT_BIRTHPLACE - 1]
        else:
            birthplace = row[COL_PASSPORT_BIRTHPLACE - 1]
        my_passport['birthplace'] = birthplace

        my_passport['created_at'] = date_converter(None)
        driver['passport'] = my_passport

        driver_license = {}
        driver_license['id'] = int(0)

        driver_license['image1'] = "Фото передней стороны"
        driver_license['image1_confirm_id'] = ""
        driver_license['image1_confirm'] = ""
        driver_license['image1_url'] = ""
        driver_license['image2'] = "Фото задней стороны"
        driver_license['image2_confirm_id'] = ""
        driver_license['image2_confirm'] = ""
        driver_license['image2_url'] = ""

        driver_license['number'] = "0000000000"
        driver_license['issued_at'] = date_converter(None)
        driver_license['finished_at'] = date_converter(None)
        driver_license['created_at'] = date_converter(None)
        driver['driver_license'] = driver_license

        drivers.append(driver)
        willz_client['drivers'] = drivers

        print(json.dumps(willz_client))
        apiRequestor = ApiRequestor()
        response = apiRequestor.post_new_client(json.dumps(willz_client))
        index += 1

# do_import()
