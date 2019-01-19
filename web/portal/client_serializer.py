from rest_framework import serializers
from web.portal.models import *
import datetime


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('individual','passport','driver_license','title', 'url')


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ('id','individual',
                  'number', 'issued_at', 'issued_by', 'address_registration', 'division_code', 'birthplace')


class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = ('id','individual', 'number', 'issued_at')


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = (
            'id', 'client', 'last_name', 'first_name', 'middle_name', 'email', 'phone', 'gender', 'birthday')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'willz', 'created_at')

