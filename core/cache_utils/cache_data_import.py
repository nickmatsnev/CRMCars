import mpu.io
import json
import sys
import os
from django.core import serializers
import django.conf



django.conf.ENVIRONMENT_VARIABLE = "DJANGO_SECOND_SETTINGS_MODULE"

os.environ.setdefault("DJANGO_SECOND_SETTINGS_MODULE", "portal.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from portal.models import CacheData
from portal.serializers.module_serializer import CacheDataValidator


print('Start import procedure')

file_path = os.path.dirname(os.path.realpath(__file__)) + '\\db_cache.json'
exists = os.path.isfile(file_path)

if exists:
    try:
        queryset_text = mpu.io.read(file_path)
        queryset_json = json.loads(queryset_text)

        serializer = CacheDataValidator(data=queryset_json, many=True)

        if serializer.is_valid():
            CacheData.objects.all().delete()
            serializer.save()
            print('DB updated sucessfully')

            print ('Press Y if you want to delete actual DB export file or press any key to continue')
            text = sys.stdin.readline()
            if text=='Y\n':
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print('Export file deleted successfully')

            print('Complete')
        else:
            print('File is not correct')

    except Exception as e:
        print(str(e))
        print('Failed')

else:
    print('No file in directory')


