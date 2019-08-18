from rest_framework import serializers

from core.lib import constants
from portal.models import *
from portal.serializers.client_serializer import  *

import datetime


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','primary_scoring','other_scoring')


class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','primary_scoring','other_scoring')


class ProductUpdateSerializer(serializers.Serializer):
    product = serializers.CharField(max_length=30)


class ContentUpdateSerializer(serializers.Serializer):
    raw_content = serializers.CharField(max_length=None)
