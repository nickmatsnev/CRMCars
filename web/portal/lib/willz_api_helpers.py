import sys

sys.path.append('../')

from core.lib.api import ApiRequestor
from portal.lib.client_api_helpers import *


def new_willz_client(request):
    data = request.data
    raw_json = json.dumps(data)
    model = RawClientData.objects.create(payload=raw_json)
    model.save()

    resp = json.dumps({constants.NAME_MESSAGE_TYPE: constants.CLIENT_RAW_CREATED_MESSAGE,
                       constants.NAME_BODY: json.dumps({'raw_client_id': model.id})})

    ApiRequestor(request).send_message(resp)

    return status.HTTP_201_CREATED
