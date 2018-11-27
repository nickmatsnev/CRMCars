from django.shortcuts import *



def index(request):
  return render(request, 'index.html',
      { 'username': request.user.username if request.user.is_authenticated else "",
        'page_active': 0 })

