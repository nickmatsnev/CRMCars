import sys

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from rest_framework.response import Response
from web.portal.models import *

from core.lib.modules import ParserModule, get_subtype_by_module_type, get_normal_serializer_by_module_type, \
    get_read_serializer_by_module_type
from core.lib.runtime_logger_helper import log


def get_module_parameters(pk, params):
    module_type = params['module_type']
    module_db = Module.objects.get(id=pk)
    module = module_type(module_db.path)
    return module.get_available_parameters()


def get_module_by_id_type(pk, params):
    module_type = params['module_type']
    module = Module.objects.get(id=pk)
    return get_read_serializer_by_module_type(module_type)(module, many=False).data;


def set_module_is_active_by_id_type(pk, params):
    module_type = params['module_type']
    module = Module.objects.get(id=pk)
    module.is_active = params['is_active']
    module.save()
    return get_normal_serializer_by_module_type(module_type)(module, many=False).data


def standard_get_by_pk(request, pk, f_try_with_pk, **f_try_parameters_after_pk):
    current_status = status.HTTP_200_OK
    try:
        res = f_try_with_pk(pk, f_try_parameters_after_pk)
    except BaseException as e:
        current_status = status.HTTP_204_NO_CONTENT
        log(e)
    finally:
        return Response(status=current_status, data=res)
