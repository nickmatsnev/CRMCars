from rest_framework import serializers

from core.lib import constants
from portal.models import *


import datetime


class ParserModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('name','path')

    def create(self, validated_data):
        module = Module.objects.create(type='Parser',is_active=True, create_time=datetime.datetime.now(),
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
        module = Module.objects.create(type='Scoring',is_active=True, create_time=datetime.datetime.now(),
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
        module = Module.objects.create(type='Source', is_active=True, create_time=datetime.datetime.now(),
                                       **validated_data)
        return module


class SourceGetModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id','name','path','is_active','create_time','credentials')

