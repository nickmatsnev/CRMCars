import sys
sys.path.append('../')

from django.shortcuts import *


def index(request):
  return render(request, 'index.html')

