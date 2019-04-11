import json

from portal.models import *
from core.lib import message_sender
from core.lib import constants
from rest_framework import status
from core.lib.api import ApiRequestor
from portal.lib.client_api_helpers import *


def new_willz_client(request):
    data = request.data;
    raw_json = json.dumps(data)
    model = RawClientData.objects.create(payload=raw_json)
    model.save()
    # TODO REFACTOR STRING CONSTANTS
    resp = json.dumps({'message_type': constants.CLIENT_RAW_CREATED_MESSAGE,
                       'body': json.dumps({'raw_client_id': model.id})})

    ApiRequestor(request).send_message(resp)

    return status.HTTP_201_CREATED
