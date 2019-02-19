from rest_framework import serializers

from core.lib import constants
from portal.models import *

import datetime


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','primary_scoring','other_scoring')


class ProductUpdateSerializer(serializers.Serializer):
    product = serializers.CharField(max_length=30)

