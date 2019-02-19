from portal.serializers.user_serializer import *
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins


class MainAPI(mixins.ListModelMixin, mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

