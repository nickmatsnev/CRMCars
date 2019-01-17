from rest_framework import serializers
from web.portal.models import *
import datetime

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
    task = TaskSerializer(many=False)
    raw_client_data = RawClientDataSerializer(many=False)
    client = ClientSerializer(many=False)

    class Meta:
        model = ClientTask
        # таск надо спрятать
        fields = ('raw_client_data', 'client', 'task')

    def create(self, validated_data):
        raw_client_data_data = validated_data.pop('raw_client_data')
        client_data = validated_data.pop('client')

        client_task = ClientTask.objects.create(**validated_data)
        new_task = Task.objects.create()

        new_task.create_time = datetime.datetime.now()
        new_task.status = "in_progress"
        new_task.task_type = 0
        client_task.task = new_task.save()

        RawClientData.objects.create(client_task=client_task, **raw_client_data_data)
        Client.objects.create(client_task=client_task, **client_data)
        return client_task


class SourceTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=False)
    source_raw_data = SourceRawDataSerializer(many=False)
    individual = IndividualSerializer(many=False)

    class Meta:
        model = SourceTask
        # таск надо спрятать
        fields = ('source_raw_data', 'individual', 'task')

    def create(self, validated_data):
        source_raw_data_data = validated_data.pop('source_raw_data')
        individual_data = validated_data.pop('individual')

        source_task = SourceTask.objects.create(**validated_data)
        new_task = Task.objects.create()

        new_task.create_time = datetime.datetime.now()
        new_task.status = "in_progress"
        new_task.task_type = 1
        source_task.task = new_task.save()

        SourceRawData.objects.create(source_task=source_task, **source_raw_data_data)
        Individual.objects.create(source_task=source_task, **individual_data)
        return source_task


class GenerationCreateSerializer(ClientSerializer):
    source_task = ClientTaskSerializer()
    individual = IndividualSerializer()

    class Meta:
        model = Generation
        fields = ('individual','source_task')

    def create(self, validated_data):
        source_task_data = validated_data.pop('source_task')
        individual_data = validated_data.pop('individual')
        generation = Generation.objects.create(**validated_data)
        generation.create_time = datetime.datetime.now()
# проверка на наличие генераций, если нет -, если есть то +1
#       if (Generation.objects.get(individual=individual)!=0:
            #+1
        #else
        generation.number=0
        SourceTask.objects.create(generation=generation, **source_task_data)
        Individual.objects.create(generation=generation, **individual_data)
        return generation


class GenerationGetSerializer(ClientSerializer):
    class Meta:
        model = Generation
        fields = ('id', 'individual', 'number', 'create_time', 'source_task')

