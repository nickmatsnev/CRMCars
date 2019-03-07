from rest_framework import serializers

from core.lib import constants
from portal.models import *

import datetime


class StatusSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=20)


class GetStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=20)

