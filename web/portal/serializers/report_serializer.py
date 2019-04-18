from rest_framework import serializers

from core.lib import constants
from portal.models import *

import datetime


class GetGeneralReportSerializer(serializers.Serializer):
    request_date = serializers.CharField(max_length=20)
    complete_date = serializers.CharField(max_length=20)
    request_number = serializers.IntegerField()
    fio_client = serializers.CharField(max_length=200)
    fio_primary_individual = serializers.CharField(max_length=200)
    processing_status =  serializers.CharField(max_length=200)
    check_status =  serializers.CharField(max_length=200)
    company_name = serializers.CharField(max_length=50)
    product_name = serializers.CharField(max_length=50)
    fio_operator = serializers.CharField(max_length=200)


class GetAdvancedReportSerializer(serializers.Serializer):
    request_date = serializers.CharField(max_length=20)
    complete_date = serializers.CharField(max_length=20)
    request_number = serializers.IntegerField()
    fio_client = serializers.CharField(max_length=200)
    fio_primary_individual = serializers.CharField(max_length=200)
    processing_status =  serializers.CharField(max_length=200)
    check_status =  serializers.CharField(max_length=200)
    stop_factors = serializers.CharField(max_length=200)
    middle_factors = serializers.CharField(max_length=200)
    company_name = serializers.CharField(max_length=50)
    product_name = serializers.CharField(max_length=50)
    fio_operator = serializers.CharField(max_length=200)
