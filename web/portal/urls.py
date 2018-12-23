import sys
sys.path.append('../')


from django.conf.urls import *
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

from web.portal.index import *
from web.portal import api

router = routers.DefaultRouter()

schema_view = get_swagger_view(title='Willz API')

router.register(r'api/clients', api.ClientViewSet)

router.register(r'api/licenses', api.LicenseViewSet)

urlpatterns = [

    url(r'^$', index),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'listclients/', api.ListClients.as_view()),
#manual created json api method
    url(r'plainapi/hello_world',api.hello_world),
    url(r'swagger', schema_view)


 ]
