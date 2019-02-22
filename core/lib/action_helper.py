import json

from core.lib import api_requestor

def add_action(client_id, action_type, processor, payload=""):
    action = {}
    action['processor'] = processor
    action['action_type'] = action_type
    action['payload'] = payload
    response = api_requestor.post('/client/{0}/add_action'.format(client_id), json.dumps(action))
    return response


def add_action_individual(individual_id, action_type, processor, payload=""):
    request = api_requestor.request('/individual/{0}/'.format(individual_id))
    return add_action(request['client'],action_type, processor, payload)