from django.conf.urls import *

from portal.index import *
from portal.api import *

urlpatterns = [

    url(r'^$', index, name="index"),
    url(r'api/tasks/create/', api_create, name="api_create"),

 ]
