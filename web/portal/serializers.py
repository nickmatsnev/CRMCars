
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
            'last_name', 'first_name', 'middle_name', 'email', 'phone', 'gender', 'birthday', 'passport',
            'driver_license')

    def create(self, validated_data):
        passport_data = validated_data.pop('passport')
        passport = Passport.objects.create(passport_data)
        driver_license_data = validated_data.pop('driver_license')
        driver_license = DriverLicense.objects.create(driver_license_data)
        individual_obj = Individual.objects.create(passport=passport, driver_license=driver_license, **validated_data)

        return individual_obj


class ClientSerializer(serializers.ModelSerializer):
    primary_individual = IndividualSerializer(many=False)

    class Meta:
        model = Client
        fields = ('willz_id', 'created_at', 'primary_individual')

    def create(self, validated_data):
        primary_individual_data = validated_data.pop('primary_individual')
        individual = Individual.objects.create(**primary_individual_data)
        client = Client.objects.create(primary_individual=individual, **validated_data)

        return client


#отсюда начал
class ClientTaskSerializer(serializers.ModelSerializer):
    pass_images = ImageSerializer(many=True)

    class Meta:
        model = ClientTask
        fields = ('raw_client_data', 'client')

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task



class SourceTaskSerializer(serializers.ModelSerializer):
#не понимаю как правильно дальше
    pass_images = ImageSerializer(many=True)

    class Meta:
        model = SourceTask
        fields = (
            'number', 'issued_at', 'issued_by', 'address_registration', 'division_code', 'birthplace', 'pass_images')

    def create(self, validated_data):
        images = validated_data.pop('pass_images')
        passport = Passport.objects.create(**validated_data)
        for image_data in images:
            Image.objects.create(passport=passport, **image_data)
        return passport


class ChecksTaskSerializer(serializers.ModelSerializer):
    pass_images = ImageSerializer(many=True)

    class Meta:
        model = ChecksTask
        fields = (
            'number', 'issued_at', 'issued_by', 'address_registration', 'division_code', 'birthplace', 'pass_images')

    def create(self, validated_data):
        images = validated_data.pop('pass_images')
        passport = Passport.objects.create(**validated_data)
        for image_data in images:
            Image.objects.create(passport=passport, **image_data)
        return passport


class ScoringTaskSerializer(serializers.ModelSerializer):
    pass_images = ImageSerializer(many=True)

    class Meta:
        model = ScoringTask
        fields = (
            'number', 'issued_at', 'issued_by', 'address_registration', 'division_code', 'birthplace', 'pass_images')

    def create(self, validated_data):
        images = validated_data.pop('pass_images')
        passport = Passport.objects.create(**validated_data)
        for image_data in images:
            Image.objects.create(passport=passport, **image_data)
        return passport


class TaskSerializer(serializers.ModelSerializer):
    clientTask = ClientTaskSerializer(many=True)
    sourceTask = SourceTaskSerializer(many=True)
    checksTask = ChecksTaskSerializer(many=True)
    scoringTask = ScoringTaskSerializer(many=True)

    class Meta:
        model = Task
        fields = ('create_time', 'finish_time', 'processor', 'status')

    def create(self, validated_data):
        primary_individual_data = validated_data.pop('primary_individual')
        individual = Individual.objects.create(**primary_individual_data)
        client = Client.objects.create(primary_individual=individual, **validated_data)

        return client