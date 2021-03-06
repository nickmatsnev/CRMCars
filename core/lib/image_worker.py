from datetime import datetime
from django.conf import settings
import hashlib
import os
from portal.settings import STATICFILES_DIRS

def __get_hex_name(file_name, user_id):
    name = f'{user_id}{datetime.now().strftime("%d.%m.%Y_%H:%M:%S")}{file_name}'
    hash_object = hashlib.md5(name.encode('utf8'))
    hex_dig = hash_object.hexdigest()
    return  hex_dig


def __save_file(file, path, hex_name):
    filename, file_extension = os.path.splitext(file.name)

    full_path = os.path.join(STATICFILES_DIRS[0], path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    full_file_path = os.path.join(full_path,hex_name+file_extension)

    with open(full_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return os.path.join(path,hex_name+file_extension)


def save_photo(file, user_id):
    hex_name = __get_hex_name(file.name, user_id)
    path = 'images'
    return __save_file(file, path, hex_name)

