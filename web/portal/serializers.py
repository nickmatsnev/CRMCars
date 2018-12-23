import sys
sys.path.append('../')

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from web.portal.models import Client,License




# Serializers define the API representation.
#hyperlinked means url is included for this method instead of id
class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('url','id','willz_id')

    def get_client_willz_id_with_id1(self):
        obj = Client.objects.filter(id=1).last()
        return obj.willz_id


class LicenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = License
        fields = ('url','id','number')
