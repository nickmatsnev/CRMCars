from django.contrib.auth.decorators import login_required
from django.shortcuts import *

@login_required(login_url="signin")
def client_inspect(request):
  return render(request, 'concrete/client_inspect.html', {'title': 'в процессе '},
      {
          #'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })

@login_required(login_url="signin")
def clients_list(request):
  return render(request, 'concrete/clients_list.html', {'title': 'Список заявок'},
      {
          #'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })
@login_required(login_url="signin")
def client_scoring(request):
  return render(request, 'concrete/client_scoring.html', {'title': 'Скоринг клиента'},
      {
          #'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })
@login_required(login_url="signin")
def source(request):
  return render(request, 'concrete/source.html', {'title': 'Ресурс//Source'},
      {
          #'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })

@login_required(login_url="signin")
def userpage(request):
  return render(request, 'concrete/user_page.html', {'title': 'Страница заявки №6'},
      {
          #'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })




