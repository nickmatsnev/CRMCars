from rest_framework import serializers

from core.lib import constants
from portal.models import *
from portal.serializers.module_serializer import  *

import datetime


class PassportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportImage
        fields = ('title', 'url')


class PassportSerializer(serializers.ModelSerializer):
    images = PassportImageSerializer(many=True)

    class Meta:
        model = Passport
        fields = ('number', 'issued_at', 'issued_by', 'address_registration', 'division_code', 'birthplace', 'images')


class DriverLicenseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicenseImage
        fields = ('title', 'url')


class DriverLicenseSerializer(serializers.ModelSerializer):
    images = DriverLicenseImageSerializer(many=True)

    class Meta:
        model = DriverLicense
        fields = ('number', 'issued_at', 'images')


class IndividualSerializer(serializers.ModelSerializer):
    passport = PassportSerializer()
    driver_license = DriverLicenseSerializer()

    class Meta:
        model = Individual
        fields = ('id', 'primary', 'last_name', 'first_name', 'middle_name', 'email', 'phone', 'gender',
                  'birthday', 'passport', 'driver_license')


class ClientSerializer(serializers.ModelSerializer):
    individuals = IndividualSerializer(many=True)

    class Meta:
        model = Client
        fields = ('id','willz', 'created_at', 'individuals')

    def create(self, validated_data):
        individuals_data = validated_data.pop('individuals')
        client = Client.objects.create( **validated_data)

        list_of_individuals_id = []
        Generation.objects.create(client=client, number=1, create_time=datetime.datetime.now())

        for individual_data in individuals_data:
            passport_data = individual_data.pop('passport')
            driver_license_data = individual_data.pop('driver_license')

            individual = Individual.objects.create(client=client, **individual_data)


            passport_images_data = passport_data.pop('images')
            passport = Passport.objects.create(individual=individual, **passport_data)

            for passport_image_data in passport_images_data:
                PassportImage.objects.create(passport=passport, **passport_image_data)

            driver_license_images_data = driver_license_data.pop('images')
            driver_license = DriverLicense.objects.create(individual=individual, **driver_license_data)

            for driver_license_image_data in driver_license_images_data:
                DriverLicenseImage.objects.create(driver_license=driver_license,
                                                  **driver_license_image_data)

        return client


#TODO дописать обновление с + генерация
    def update(self, validated_data):
        individuals_data = validated_data.pop('individuals')
        client = Client.objects.create(**validated_data)
        #Product.objects.create(client=client,name='Willz')
        Generation.objects.create(client=client, number=1, create_time=datetime.datetime.now())

        for individual_data in individuals_data:
            passport_data = individual_data.pop('passport')
            driver_license_data = individual_data.pop('driver_license')

            individual = Individual.objects.create(client=client, **individual_data)


            passport_images_data = passport_data.pop('images')
            passport = Passport.objects.create(individual=individual, **passport_data)

            for passport_image_data in passport_images_data:
                PassportImage.objects.create(passport=passport, **passport_image_data)

            driver_license_images_data = driver_license_data.pop('images')
            driver_license = DriverLicense.objects.create(individual=individual, **driver_license_data)

            for driver_license_image_data in driver_license_images_data:
                DriverLicenseImage.objects.create(driver_license=driver_license,
                                                  **driver_license_image_data)

        return client


class IndividualGetSerializer(serializers.ModelSerializer):
    passport = PassportSerializer()
    driver_license = DriverLicenseSerializer()

    class Meta:
        model = Individual
        fields = ('id','primary', 'last_name', 'first_name', 'middle_name', 'email', 'phone', 'gender',
                  'birthday', 'passport', 'driver_license')


class ClientGetSerializer(serializers.ModelSerializer):
    individuals = IndividualGetSerializer(many=True)
    product = ProductSerializer(many=False)

    class Meta:
        model = Client
        fields = ('id', 'willz', 'created_at', 'individuals', 'product')


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('create_time', 'processor', 'action_type', 'payload')


class NewActionSerializer(serializers.Serializer):
    processor = serializers.CharField()
    action_type = serializers.CharField()
    payload = serializers.CharField(min_length=0,required=False)


class GenerationSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True)

    class Meta:
        model = Generation
        fields = ('number','create_time','actions')


class ViewTableSerializer(serializers.Serializer):
    list_of_fields = serializers.CharField(max_length=255, required=True)

