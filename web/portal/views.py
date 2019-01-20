from django.contrib.auth.decorators import login_required
from django.shortcuts import *

@login_required(login_url="signin")
def client_inspect(request):
  return render(request, 'concrete/client_inspect.html',
      {
          #'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })

@login_required(login_url="signin")
def clients_list(request):
  return render(request, 'concrete/clients_list.html',
      {
          #'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })




