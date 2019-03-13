import ast
import sys

from portal.models import Module

sys.path.append('../../')
sys.path.append('..')
from rest_framework import status
from portal.lib.module_serializer_helper import get_read_serializer_by_module_type, get_normal_serializer_by_module_type
from core.lib import module_save_helper
from core.lib.modules import *
from rest_framework.response import Response
from portal.serializers.module_serializer import *


def get_list_of_names(module_type):
    list_of_names = []
    queryset = Module.objects.filter(type=module_type, is_active=True)

    for item in queryset:
        list_of_names.append(item.name)
    return list_of_names


def get_module_data_by_type_name(pk, module_type, module_name):
    queryset = ModuleData.objects.filter(individual=pk, name=module_name)
    if queryset.count() == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)

    queryset = queryset.get()
    list_of_names = get_list_of_names(module_type)
    if queryset.name in list_of_names:
        return Response(queryset.raw_data)

    return Response(status=status.HTTP_204_NO_CONTENT)


def get_module_meta_by_type_name(pk, module_type, module_name):
    queryset = ModuleData.objects.filter(individual=pk, name=module_name)
    if queryset.count() == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)

    queryset = queryset.get()
    list_of_names = get_list_of_names(module_type)
    if queryset.name in list_of_names:
        serializer_class = ModuleMetaSerializer(queryset, many=False)
        return Response(serializer_class.data)

    return Response(status=status.HTTP_204_NO_CONTENT)


def set_module_data_by_type_name(json_data, pk, module_type, module_name):
    list_of_names = get_list_of_names(module_type)

    if module_name in list_of_names:
        queryset = ModuleData.objects.filter(individual=pk, name=module_name)

        if queryset.count() == 0:
            queryset = ModuleData.objects.create(individual=pk, raw_data=json_data,
                                                 name=module_name, create_time=datetime.datetime.now())
            response_status = status.HTTP_201_CREATED
        else:
            pk = queryset.get().pk
            ModuleData.objects.filter(pk=pk).update(raw_data=json_data,
                                                    create_time=datetime.datetime.now())
            queryset = ModuleData.objects.get(pk=pk)
            response_status = status.HTTP_202_ACCEPTED

        serializer_class = ModuleDataSerializer(queryset, many=False)
        return Response(status=response_status, data=serializer_class.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def get_module_data_list_by_type(pk, module_type):
    list_of_names = get_list_of_names(module_type)
    queryset = ModuleData.objects.filter(individual=pk).order_by('create_time')

    if queryset.count() == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        response_data = {}
        counter = 1

        for current_module in queryset:
            if current_module.name in list_of_names:
                json_data = {}
                try:
                    json_data = ast.literal_eval(current_module.raw_data)
                except:
                    json_data = {'incorrect_json': current_module.raw_data}
                finally:
                    response_data['{0}'.format(current_module.name)] = json_data
                    counter += 1

    return Response(response_data)


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


def get_module_by_name(module_type, module_name):
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
    response_status = status.HTTP_202_ACCEPTED
    response_data = ""

    dest_path = get_path_by_module_type(module_type)
    path = module_save_helper.save_file_from_request(request, dest_path)
    serializer_class = get_normal_serializer_by_module_type(module_type)
    serializer_data = module_save_helper.prepare_module_item(path)

    serializer = serializer_class(data=serializer_data)
    if serializer.is_valid():
        module_name = serializer.validated_data['name']
        queryset = Module.objects.filter(name=module_name)
        if queryset.count()==0:
            serializer.save()
            response_data = "Module with type {0} saved successfully".format(module_type)
        else:
            response_status = status.HTTP_403_FORBIDDEN
    else:
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(status=response_status, data=response_data)


def delete_module(module_type, module_name):
    queryset = Module.objects.filter(type=get_subtype_by_module_type(module_type),name=module_name)
    if queryset.count()==0:
        return  Response(status=status.HTTP_204_NO_CONTENT)
    queryset.delete()
    return Response(status=status.HTTP_200_OK, data="Module {0} deleted successfully".format(module_name))


def get_module_parameters(module_type, pk):
    module_db = Module.objects.get(id=pk, type=get_subtype_by_module_type(module_type))
    module = get_class_by_module_type(module_type)(module_db.path)
    return module.get_available_parameters()


def set_module_is_active_by_id_type(module_type, pk, active_or_not):
    module = Module.objects.get(id=pk, type=get_subtype_by_module_type(module_type))
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


def post_test(module_type, request):
    serializer_class = get_normal_serializer_by_module_type(module_type)
    serializer = serializer_class(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return status.HTTP_202_ACCEPTED
    return status.HTTP_400_BAD_REQUEST


def get_credentials(module_type, pk):
    response = {}
    resp_status = status.HTTP_200_OK

    if Module.objects.filter(id=pk).count() == 0:
        credentials = ""
        resp_status = status.HTTP_204_NO_CONTENT
    else:
        module = Module.objects.get(id=pk)
        if module.type != get_subtype_by_module_type(module_type):
            credentials = ""
            resp_status = status.HTTP_400_BAD_REQUEST
        else:
            credentials = module.credentials

    response['credentials'] = credentials
    return Response(status=resp_status, data=response['credentials'])


def set_credentials(module_type, pk, credentials):
    response = {}
    resp_status = status.HTTP_200_OK

    if Module.objects.filter(id=pk).count() == 0:
        credentials = ""
        resp_status = status.HTTP_204_NO_CONTENT
    else:
        module = Module.objects.get(id=pk)
        if module.type != get_subtype_by_module_type(module_type):
            credentials = ""
            resp_status = status.HTTP_400_BAD_REQUEST
        else:
            module.credentials = credentials
            module.save()

    response['credentials'] = credentials
    return Response(status=resp_status, data=response['credentials'])


def get_info(individual, generation_number,module_type,module_name,field_main,field_sub=''):
    list_of_names = get_list_of_names(module_type)

    if module_name in list_of_names:
        queryset = ModuleData.objects.filter(individual=individual, generation=generation_number)
        if queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        queryset = queryset.get()
        serializer_class = ModuleDataSerializer(queryset, many=False)
        my_data = {}
        try:
            json_data = json.loads(serializer_class.data['raw_data'])
            if field_sub == '':
                my_data = json_data[field_main]
            else:
                my_data = json_data[field_main][field_sub]
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        finally:
            if my_data != {}:
                return Response(data=my_data)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def get_list_info(individual,generation_number,module_type,field_main,field_sub=''):
    list_of_names = get_list_of_names(module_type)
    my_list = []

    for module_name in list_of_names:
        queryset = ModuleData.objects.filter(individual=individual, generation=generation_number)

        if queryset.count() != 0:
            queryset = queryset.get()
            serializer_class = ModuleDataSerializer(queryset, many=False)
            my_data = {}
            try:
                json_data = json.loads(serializer_class.data['raw_data'])
                if field_sub == '':
                    my_data = json_data[field_main]
                else:
                    my_data = json_data[field_main][field_sub]
            except:
                my_data = {}
            finally:
                if my_data != {}:
                    my_json = {}
                    my_json[module_name] = my_data
                    my_list.append(my_json)

    return Response(data=my_list)


def get_generation_number(individual_id, generation_id_or_current):
    generation_number = 0

    if generation_id_or_current.isdigit():
        generation_number = generation_id_or_current
    elif generation_id_or_current == 'current':
        generations = Generation.objects.filter(individual_id=individual_id)
        for gen in generations:
            if gen.is_archive == False:
                generation_number = gen.number

    return generation_number