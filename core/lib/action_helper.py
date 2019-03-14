import json

from core.lib import api_requestor


def add_action(individual_id, action_type, processor, payload="empty"):
    action = {}
    action['processor'] = processor
    action['action_type'] = action_type
    action['payload'] = payload
    dumped_data = json.dumps(action)
    response = api_requestor.post('/individual/{0}/cur_gen/add_action/'.format(individual_id), dumped_data)
    return json.loads(response.content)

