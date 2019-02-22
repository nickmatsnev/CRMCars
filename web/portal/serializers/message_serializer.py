from rest_framework import serializers
import sys

sys.path.append('../../')
sys.path.append('../')
from core.lib import constants


class BusMessageSerializer(serializers.Serializer):
    MESSAGE_CHOICES = (
        (constants.CLIENT_RAW_CREATED_MESSAGE),
        (constants.INDIVIDUAL_SCORING_PROCESS),
        (constants.INDIVIDUAL_SCORING_PROCESS)
    )
    message_type = serializers.ChoiceField(MESSAGE_CHOICES)
    body = serializers.CharField()