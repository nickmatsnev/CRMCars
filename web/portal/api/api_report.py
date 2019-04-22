import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from portal.serializers.report_serializer import *
from drf_yasg import openapi
from core.lib import message_sender
from portal.lib.status_api_helpers import *
from core.lib.modules import ScoringModule, SourceModule
from portal.models import *
from core.lib.api import ApiRequestor
from portal.lib.product_api_helpers import get_product_id_for_individual
from django.contrib.auth.models import User
from portal.lib.report_api_helpers import get_standard_report


#AdvancedReport
class GeneralReport(APIView):
    @swagger_auto_schema(operation_description='Get table of values', responses={200: GetGeneralReportSerializer,
                                                                                   })
    def get(self, request,):

        return Response(get_standard_report(request))


class AdvancedReport(APIView):
    @swagger_auto_schema(operation_description='Get table of values', responses={200: GetAdvancedReportSerializer,
                                                                             })
    def get(self, request, ):
        return Response(get_standard_report(request,True))


