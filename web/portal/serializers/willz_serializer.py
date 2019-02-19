from rest_framework import serializers

from core.lib import constants
from portal.models import *
import datetime


class RawClientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClientData
        fields = ('__all__')

