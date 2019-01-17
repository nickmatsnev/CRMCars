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
        fields = ('id', 'willz_id', 'created_at')


class RawClientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('id', 'payload')


class SourceRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('id', 'payload', 'individual', 'source')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('create_time', 'finish_time', 'processor', 'status', 'task_type')


class ClientTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTask
        fields = ('raw_client_data', 'client')

  #  def create(self, validated_data):
  #      task = TaskSerializer
  #       status = in_progress...


class CreateClientTaskSerializer(ClientTaskSerializer):
    task = TaskSerializer(many=False)
    raw_client_data = RawClientDataSerializer(many=False)
    client = ClientSerializer(many=False)


class UpdateClientTaskSerializer(ClientTaskSerializer):
    task = TaskSerializer(many=False)
    raw_client_data = RawClientDataSerializer(many=False)
    client = ClientSerializer(many=False)



