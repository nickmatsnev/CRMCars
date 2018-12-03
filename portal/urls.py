from django.conf.urls import *

from portal.index import *
from portal.api import *

urlpatterns = [

    url(r'^$', index),
    url(r'api/clients/create/', api_create),

 ]
