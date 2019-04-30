#!/usr/bin/env python3
import sys

sys.path.append('../../')
sys.path.append('../../web')

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.portal.settings')
django.setup()

from core.utils import excel_to_request
from core.lib.api import ApiRequestor
from core.lib import constants

from django.contrib.auth.models import User

try:
    print('Creating admin user')
    admin_user = User.objects.filter(username=constants.ADMIN_USERNAME)
    if admin_user.count() == 0:
        user = User.objects.create_user(username=constants.ADMIN_USERNAME,
                                        email='admin@willz-dev.ru',
                                        password=constants.ADMIN_PASSWORD)
        user.save()
    print('uploading clients')
    excel_to_request.do_import(5)

    print('uploading modules')
    ApiRequestor().do_module_upload_from_file("source", "../sources/contur_focus_source.py")
    ApiRequestor().do_module_upload_from_file("source", "../sources/infosfera_source.py")
    ApiRequestor().do_module_upload_from_file("source", "../sources/scorista_source.py")
    ApiRequestor().do_module_upload_from_file("source", "../sources/nbki_source.py")

    ApiRequestor().do_module_upload_from_file("parser", "../parsers/contur_focus_parser.py")
    ApiRequestor().do_module_upload_from_file("parser", "../parsers/infosfera_parser.py")
    ApiRequestor().do_module_upload_from_file("parser", "../parsers/scorista_parser.py")
    ApiRequestor().do_module_upload_from_file("parser", "../parsers/nbki_parser.py")

    ApiRequestor().do_module_upload_from_file("scoring", "../scoring/all_scoring.py")




except Exception as e:
    print(str(e))
    print('Failed')
