import sys
sys.path.append('../')


from django.conf.urls import *

from web.portal.index import *
from web.portal.api import *

urlpatterns = [

    url(r'^$', index),
    url(r'api/clients/create/', api_create),

 ]
