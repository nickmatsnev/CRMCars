from rest_framework import serializers
from web.portal.models import *
from web.portal.client_serializer  import *
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


class RawClientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('id', 'payload')


class SourceRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('id', 'payload', 'individual', 'source')



