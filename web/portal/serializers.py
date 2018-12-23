from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from web.portal.models import *

# Serializers define the API representation.
#hyperlinked means url is included for this method instead of id

class PassportSerializer(serializers.HyperlinkedModelSerializer):
    pass_images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Passport
        fields = ('number','issued_at','issued_by','address_registration','division_code','birthplace')


class LicenseSerializer(serializers.HyperlinkedModelSerializer):
    lcns_images = serializers.StringRelatedField(many=True)

    class Meta:
        model = License
        fields = ('number', 'issued_at')


class IndividualSerializer(serializers.HyperlinkedModelSerializer):
    passports = serializers.StringRelatedField(many=True)
    licenses = serializers.StringRelatedField(many=True)

    class Meta:
        model = Individual
        fields = ('lastname', 'firstname', 'middlename', 'email', 'phone', 'gender', 'birthday')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('passport', 'license', 'title', 'url')


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    clients = serializers.StringRelatedField(many=True)

    class Meta:
        model = Client
        fields = ('willz_id', 'created_at')
