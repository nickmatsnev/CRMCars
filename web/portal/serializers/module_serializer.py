from rest_framework import serializers
import json
from core.lib import constants
from portal.models import *


import datetime


class ParserModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name','path')

    def create(self, validated_data):
        module = Module.objects.create(type='parser', is_active=True, create_time=datetime.datetime.now(),
                                       **validated_data)
        return module


class ParserGetModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id','name','path','is_active','create_time')


class ScoringModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name','path')

    def create(self, validated_data):
        module = Module.objects.create(type='scoring', is_active=True, create_time=datetime.datetime.now(),
                                       **validated_data)
        return module


class ScoringGetModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id','name','path','is_active','create_time')


class SourceModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name','path','credentials')

    def create(self, validated_data):
        module = Module.objects.create(type='source', is_active=True, create_time=datetime.datetime.now(),
                                       **validated_data)
        return module


class SourceGetModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id','name','path','is_active','create_time','credentials')


class ModuleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleData
        fields = ('id','individual','raw_data', 'create_time')


class ModuleMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleData
        fields = ('id','individual','create_time')


class ModuleDataListSerializer(serializers.Serializer):
    type_name_N = serializers.CharField(max_length=20)


class ModuleUpdateDataSerializer(serializers.Serializer):
    raw_data = serializers.CharField(max_length=20)


class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleData
        fields = ('id','individual','raw_data', 'create_time')


class CacheDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CacheData
        fields = ('type_of_request', 'url', 'data', 'headers')

