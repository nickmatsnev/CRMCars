import json

from core.lib import api_requestor

def add_action(client, action_type, processor, payload=""):
    action = {}
    action['processor'] = processor
    action['action_type'] = action_type
    action['payload'] = payload
    dumped_data = json.dumps(action)
    response = api_requestor.post('/client/{0}/add_action/'.format(client), dumped_data)
    return response


def add_action_individual(individual, action_type, processor, payload=""):
    request = api_requestor.request('/individual/{0}'.format(individual))
    return add_action(request['client'],action_type, processor, payload)