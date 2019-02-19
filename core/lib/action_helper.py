import json

from core.lib import api_requestor

def add_action(client_id, action_type, processor, payload=""):
    action = {}
    action['processor'] = processor
    action['action_type'] = action_type
    action['payload'] = payload
    response = api_requestor.post('/client/{0}/add_action'.format(client_id), json.dumps(action))
    return response

