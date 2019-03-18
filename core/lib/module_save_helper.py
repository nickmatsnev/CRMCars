import os
from core.lib import modules
from django.apps import apps


def save_file_from_request(request, dest_path):
    uploaded_file = request.FILES['file']
    path = os.path.join(apps.get_app_config('portal').path, dest_path)

    destination = open(os.path.join(path, uploaded_file.name), 'wb+')
    for chunk in uploaded_file.chunks():
        destination.write(chunk)
    destination.close()

    return os.path.abspath(destination.name)


def prepare_module_item(path):
    parser_m = modules.ParserModule(path)

    item = {}
    item['name'] = parser_m.get_module_name()
    item['path'] = path
    return item
