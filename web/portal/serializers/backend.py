from rest_framework import serializers

from lib import constants
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
        fields = ('id','individual','number', 'issued_at')


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('create_time', 'processor', 'action_type', 'payload')


class NewActionSerializer(serializers.Serializer):
    individual = serializers.IntegerField()
    processor = serializers.CharField()
    action_type = serializers.CharField()
    payload = serializers.CharField()


class BusMessageSerializer(serializers.Serializer):
    MESSAGE_CHOICES = (
        (constants.CLIENT_RAW_CREATED_MESSAGE),
        (constants.CLIENT_PROCESSED_MESSAGE),
    )
    message_type = serializers.ChoiceField(MESSAGE_CHOICES)
    body = serializers.CharField()



class GenerationSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True)

    class Meta:
        model = Generation
      #  fields = ('individual','number','create_time','status','client_task','scoring_task','source_task','checks_task')
        fields = ('individual','number','create_time','actions')


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ('id','primary','client', 'last_name', 'first_name', 'middle_name', 'email', 'phone', 'gender',
                  'birthday')

    def create(self, validated_data):
        individual = Individual.objects.create(**validated_data)
        Generation.objects.create(individual=individual,
                                  number=0,
                                  create_time=datetime.datetime.now())
        return individual


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id','willz', 'created_at')


class ImageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('title', 'url')


class PassportGetSerializer(serializers.ModelSerializer):
  passport_images = ImageGetSerializer(many=True)

  class Meta:
        model = Passport
        fields = ('number', 'issued_at', 'issued_by', 'address_registration', 'division_code', 'birthplace',
                  'passport_images')


class DriverLicenseGetSerializer(serializers.ModelSerializer):
  driver_license_images = ImageGetSerializer(many=True)

  class Meta:
        model = DriverLicense
        fields = ('number', 'issued_at','driver_license_images')


class IndividualGetSerializer(serializers.ModelSerializer):
    passport = PassportGetSerializer(many=False)
    driver_license = DriverLicenseGetSerializer(many=False)

    class Meta:
        model = Individual
        fields = ('id', 'primary', 'last_name', 'first_name', 'middle_name', 'email', 'phone', 'gender', 'birthday',
                  'passport','driver_license')


class ClientGetSerializer(serializers.ModelSerializer):
    individuals = IndividualGetSerializer(many=True)

    class Meta:
        model = Client
        fields = ('willz', 'created_at','individuals')


class RawClientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('id', 'payload')


class SourceRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('id', 'payload', 'individual', 'source')

#        def create(self, validated_data):
#            individuals_data = validated_data.pop('individuals')
#            client = Client.objects.create(**validated_data)

#            for individual_data in individuals_data:
#                individual = Individual.objects.create(client=client, **individual_data)

#                passport_data = individual_data.pop('passport')
#                passport = Passport.objects.create(individual=individual,**passport_data)
#                passport_images_data = passport_data.pop('passport_images')
#                for passport_image_data in passport_images_data:
#                    Image.objects.create(individual=individual,passport=passport,**passport_image_data)

#                driver_license_data = individual_data.pop('driver_license')
#                driver_license = DriverLicense.objects.create(individual=individual,**driver_license_data)
#                driver_license_images_data = passport_data.pop('driver_license_images')
#                for driver_license_image_data in driver_license_images_data:
#                    Image.objects.create(individual=individual,driver_license=driver_license,**driver_license_image_data)
#            return client