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


print('Start export procedure')

try:
    queryset = CacheData.objects.all()
    serializer = CacheDataValidator(queryset,many=True)

    serialized_text = json.dumps(serializer.data)
    file_path = os.path.dirname(os.path.realpath(__file__)) + '\\db_cache.json'

    if os.path.isfile(file_path):
        os.remove(file_path)

    mpu.io.write(file_path, serialized_text)
    print('File "%s" was created/updated' % file_path)
    print('Complete')

except Exception as e:
    print(str(e))
    print('Failed')


