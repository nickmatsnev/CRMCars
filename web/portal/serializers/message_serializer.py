from rest_framework import serializers

from core.lib import constants


class BusMessageSerializer(serializers.Serializer):
    MESSAGE_CHOICES = (
        (constants.CLIENT_RAW_CREATED_MESSAGE),
        (constants.CLIENT_PROCESSED_MESSAGE),
    )
    message_type = serializers.ChoiceField(MESSAGE_CHOICES)
    body = serializers.CharField()