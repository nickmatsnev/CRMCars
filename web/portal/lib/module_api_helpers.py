import sys

from portal.models import Module

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from portal.lib.module_serializer_helper import get_read_serializer_by_module_type, get_normal_serializer_by_module_type
from core.lib import module_save_helper
from core.lib.modules import *


def get_module_by_type(module_type, pk=None):
    many = True

    if pk is not None:
        many = False
        module = Module.objects.get(id=pk)
        if module.type != get_subtype_by_module_type(module_type):
            return {}
    else:
        module = Module.objects.filter(type=get_subtype_by_module_type(module_type))

    serializer = get_read_serializer_by_module_type(module_type)(module, many=many)
    return serializer.data


def get_module_by_name(module_type,module_name):
    module = Module.objects.filter(type=get_subtype_by_module_type(module_type), name=module_name)

    serializer = get_read_serializer_by_module_type(module_type)(module, many=True)
    return serializer.data


def view_module_by_type(module_type):
    modules = Module.objects.filter(type=get_subtype_by_module_type(module_type))

    items = []
    for module in modules:
        item = {}
        item['id'] = module.id
        item['name'] = module.name
        item['path'] = module.path
        item['is_active'] = module.is_active
        item['creation_time'] = module.create_time
        if module_type == "source":
            item['credentials'] = module.credentials
            module_loader = get_class_by_module_type(module_type)(module.path)
            item['module_url'] = module_loader.get_module_url()
        items.append(item)
    return items


def save_module(request, module_type):
    dest_path = get_path_by_module_type(module_type)
    path = module_save_helper.save_file_from_request(request, dest_path)
    serializer_class = get_normal_serializer_by_module_type(module_type)
    serializer_data = module_save_helper.prepare_module_item(path)
    serializer = serializer_class(data=serializer_data)

    if serializer.is_valid():
        serializer.save()
        return status.HTTP_202_ACCEPTED
    return status.HTTP_400_BAD_REQUEST


def get_module_parameters(module_type,pk):
    module_db = Module.objects.get(id=pk,type=get_subtype_by_module_type(module_type))
    module = get_class_by_module_type(module_type)(module_db.path)
    return module.get_available_parameters()


def set_module_is_active_by_id_type(module_type,pk,active_or_not):
    module = Module.objects.get(id=pk,type=get_subtype_by_module_type(module_type))
    module.is_active = active_or_not
    module.save()
    return get_normal_serializer_by_module_type(module_type)(module, many=False).data


def view_all_parameters_from_active_modules(module_type):
    modules_parameters = []
    modules = Module.objects.filter(type=get_subtype_by_module_type(module_type), is_active=True)
    for parsing_module in modules:
        parser_m = get_class_by_module_type(module_type)(parsing_module.path)
        parameters = parser_m.get_available_parameters()
        for parameter in parameters:
            new_item = {}
            new_item['source'] = parser_m.get_module_source()
            new_item['parser'] = parser_m.get_module_name()
            new_item['name'] = parameter['name']
            new_item['description'] = parameter['description']
            new_item['type'] = parameter['type']
            modules_parameters.append(new_item)
    return modules_parameters


def post_test(module_type,request):
    serializer_class = get_normal_serializer_by_module_type(module_type)
    serializer = serializer_class(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return status.HTTP_202_ACCEPTED
    return status.HTTP_400_BAD_REQUEST


