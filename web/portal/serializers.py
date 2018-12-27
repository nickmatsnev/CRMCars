from rest_framework import serializers
from web.portal.models import *


class CheckModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ('name', 'description')


class ScoreModelSerializer(serializers.HyperlinkedModelSerializer):
    check_models = CheckModelSerializer(many=True)

    class Meta:
        model = ScoreModel
        fields = ('check_models')

    def create(self, validated_data):
        check_models = validated_data.pop('check_models')
        passport = Passport.objects.create(**validated_data)
        for check in check_models:
            CheckModel.create
        return passport


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('passport', 'driver_license', 'title', 'url')


class PassportSerializer(serializers.ModelSerializer):
    pass_images = ImageSerializer(many=True)

    class Meta:
        model = Passport
        fields = (
            'number', 'issued_at', 'issued_by', 'address_registration', 'division_code', 'birthplace', 'pass_images')

    def create(self, validated_data):
        images = validated_data.pop('pass_images')
        passport = Passport.objects.create(**validated_data)
        for image_data in images:
            Image.objects.create(passport=passport, **image_data)
        return passport


class DriverLicenseSerializer(serializers.ModelSerializer):
    lcns_images = ImageSerializer(many=True)

    class Meta:
        model = DriverLicense
        fields = ('number', 'issued_at', 'lcns_images')

    def create(self, validated_data):
        images = validated_data.pop('pass_images')
        driver_license = DriverLicense.objects.create(**validated_data)
        for image_data in images:
            Image.objects.create(driver_license=driver_license, **image_data)
        return license


class IndividualSerializer(serializers.ModelSerializer):
    passport = PassportSerializer(many=False)
    driver_license = DriverLicenseSerializer(many=False)

    class Meta:
        model = Individual
        fields = (
            'id','last_name', 'first_name', 'middle_name', 'email', 'phone', 'gender', 'birthday', 'passport',
            'driver_license')

    def create(self, validated_data):
        passport_data = validated_data.pop('passport')
        passport = Passport.objects.create(passport_data)
        driver_license_data = validated_data.pop('driver_license')
        driver_license = DriverLicense.objects.create(**driver_license_data)
        individual_obj = Individual.objects.create(passport=passport, driver_license=driver_license, **validated_data)

        return individual_obj


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id','willz_id', 'created_at')



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('create_time', 'finish_time', 'processor', 'status', 'task_type')


class RawClientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('id','payload')

class ClientTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTask
        fields = ('task', 'raw_client_data', 'client')


class RetrieveClientTaskSerializer(ClientTaskSerializer):
    task = TaskSerializer(many=False)
    raw_client_data = RawClientDataSerializer(many=False)
    client = ClientSerializer(many=False)



