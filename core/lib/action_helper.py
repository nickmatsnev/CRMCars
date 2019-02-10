import json

from core.lib import api_requestor

def add_action(individual_id, action_type, processor, payload=""):
    action = {}
    action['individual']=individual_id
    action['processor'] = processor
    action['action_type'] = action_type
    action['payload'] = payload
    response = api_requestor.post('/new_action/',json.dumps(action))
    return response

