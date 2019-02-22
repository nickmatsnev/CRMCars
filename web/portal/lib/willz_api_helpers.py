import json

from portal.models import *
from core.lib import message_sender, api_requestor
from core.lib import constants
from rest_framework import status
from portal.lib.client_api_helpers import *

def new_willz_client(data):
    raw_json = json.dumps(data)
    model = RawClientData.objects.create(payload=raw_json)
    model.save()

    resp = json.dumps({'message_type': constants.CLIENT_RAW_CREATED_MESSAGE,
                               'body': json.dumps({'raw_client_id': model.id})});

    raw_data = api_requestor.post('/message/', resp)

    return status.HTTP_201_CREATED
