from django.conf.urls import *

from portal.index import *

urlpatterns = [

    url(r'^$', index, name="index"),

 ]
