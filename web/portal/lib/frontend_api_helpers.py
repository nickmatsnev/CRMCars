import sys

sys.path.append('../../')
sys.path.append('..')

from rest_framework import status
from rest_framework.response import Response

from core.lib.runtime_logger_helper import log
from core.lib.modules import get_subtype_by_module_type, SourceModule
from web.portal.models import *
from core.lib import module_save_helper


def save_module(request, params):
    path = module_save_helper.save_file_from_request(request, params['path_to_modules'])
    serializer_class = params['serializer']
    serializer = serializer_class(data=module_save_helper.prepare_module_item(path))
    if serializer.is_valid():
        serializer.save()


def standard_post(request, f_try_with_request, **f_try_parameters_after_request):
    current_status = status.HTTP_201_CREATED
    try:
        f_try_with_request(request, f_try_parameters_after_request)

    except:
        current_status = status.HTTP_400_BAD_REQUEST
    finally:
        return Response(status=current_status)


def standard_get_list(request, f_try_with_request, **f_try_parameters_after_request):
    response_data = {}
    try:
        response_data = f_try_with_request(f_try_parameters_after_request)
    except BaseException as e:
        log(e)
    finally:
        return Response(response_data)


def get_all_parameters_from_active_modules(params):
    modules_parameters = []
    module_class = params['module_type']
    modules = Module.objects.filter(type=get_subtype_by_module_type(module_class), is_active=True)
    for parsing_module in modules:
        parser_m = module_class(parsing_module.path)
        parameters = parser_m.get_available_parameters()
        for parameter in parameters:
            new_item = {}
            new_item['source'] = parser_m.get_source()
            new_item['parser'] = parser_m.get_module_name()
            new_item['name'] = parameter['name']
            new_item['description'] = parameter['description']
            new_item['type'] = parameter['type']
            modules_parameters.append(new_item)
    return modules_parameters


def get_modules(params):
    module_class = params['module_type']
    modules = Module.objects.filter(type=get_subtype_by_module_type(module_class))

    items = []
    for module in modules:
        item = {}
        item['name'] = module.name
        item['path'] = module.path
        item['is_active'] = module.is_active
        item['creation_time'] = module.create_time
        if module_class == SourceModule:
            item['credentials'] = module.credentials
            module_loader = module_class(module.path)
            item['module_url'] = module_loader.get_module_url()
        items.append(item)
    return items
