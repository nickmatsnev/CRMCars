import json
import sys

sys.path.append('../')

from web.portal.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.utils.encoding import smart_text
from core.lib import api_requestor
from core.lib import action_helper
from core.scoring.scorista import get_scorista, get_scoring, get_checks


@login_required(login_url="signin")
def clients_list(request):
    items = api_requestor.request('/front/clients/')

    return render(request, 'concrete/clients_list.html', {'items': items})


@login_required(login_url="signin")
def users_list(request):
  users = api_requestor.request('/front/users/')

  return render(request, 'concrete/users_list.html', {'items':users})


@login_required(login_url="signin")
def client_decline(request,id):
    raw_data = api_requestor.request('/front/clients/{0}/'.format(id))

    context = {'individual': raw_data['individual'], 'id': raw_data['id'], 'drivers': raw_data['drivers'],
               'history': raw_data['op_history']}

    return render(request, 'concrete/client_decline.html',context)


@login_required(login_url="signin")
def client_scoring(request,id):
    res = get_scorista()

    checks = get_checks('4518334452', '77МА051161', res)['checks']

    score = get_scoring(json.dumps({'checks': checks}, indent=4, sort_keys=False, ensure_ascii=True))

    return render(request, 'concrete/client_scoring.html',
                  {'id': id, 'score': score, 'checks': checks, 'raw_data': smart_text(res, "utf-8"),
                   'disabled': 'disabled'})

@login_required(login_url="signin")
def source(request):
  return render(request, 'concrete/source.html')


@login_required(login_url="signin")
def client_inspect(request,id):
    raw_data = api_requestor.request('/front/clients/{0}/'.format(id))

    context = {'individual': raw_data['individual'], 'id': raw_data['id'], 'drivers': raw_data['drivers'],
               'history': raw_data['op_history']}

    return render(request, 'concrete/client_inspect.html', context)


@login_required(login_url="signin")
def accept_client(request, id):
    action_helper.add_action(id, 'accepted', 'user')
    return redirect("clients_list")


@login_required(login_url="signin")
def reject_client(request, id, ):
    action_helper.add_action(id,'declined','user')
    return redirect("clients_list")



