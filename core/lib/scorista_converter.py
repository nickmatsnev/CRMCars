class AddressObject:
    index = 0
    oblast = ''
    city = ''
    street = ''
    house = ''
    building = ''
    flat = ''
    kladr = 0


def get_converted_address(text):
    text_splited = text.split(",")
    resp = AddressObject
    resp.index=0
    resp.oblast=''
    resp.city=''
    resp.street=''
    resp.house=''
    resp.building=''
    resp.flat=''
    resp.kladr=0

    cntr = 1

    for text_part in text_splited:
        text_part.replace(',', '')

        if text_part.isdigit():
            if len(text_part) == 6:
                resp.index = text_part
                cntr -= 1

        if cntr == 1:
            if text_part.__contains__('г.') or text_part.__contains__('с.') or text_part.__contains__(
                    'сел.') or text_part.__contains__('гор.') or text_part.__contains__(
                    'город ') or text_part.__contains__('д.') or text_part.__contains__(
                    'дер.') or text_part.__contains__('Москва') or text_part.__contains__('Санкт-Петербург'):
                resp.city = text_part
            else:
                resp.oblast = text_part

        elif cntr == 2:
            if resp.city == '':
                resp.city = text_part
            else:
                resp.street = text_part

        else:
            if (text_part.__contains__('г.') or text_part.__contains__('с.') or text_part.__contains__(
                    'сел.') or text_part.__contains__('гор.') or text_part.__contains__(
                    'город ') or text_part.__contains__('д.') or text_part.__contains__(
                    'дер.') or text_part.__contains__('Москва') or text_part.__contains__('Санкт-Петербург')) and resp.city == '':
                resp.city = text_part
            elif text_part.__contains__('ул.') or text_part.__contains__('у.'):
                resp.street = text_part
            elif text_part.__contains__('д.') or text_part.__contains__('дом '):
                resp.house = text_part
            elif text_part.__contains__('к.') or text_part.__contains__('корп.') or text_part.__contains__('кор.'):
                resp.building = text_part
            elif text_part.__contains__('кв.'):
                resp.flat = text_part
        cntr += 1

    return resp


class PassportObject:
    SN_serial = 0
    SN_number = 0


def get_splited_passport(number):
    number_splited = number.split(" ")
    obj = PassportObject

    cntr = len(number_splited)

    if cntr == 1:
        obj.SN_serial = number[:4]
        obj.SN_number = number[4:]

    elif cntr == 2:
        obj.SN_serial = number_splited[0]
        obj.SN_number = number_splited[1]

    elif cntr == 3:
        obj.SN_serial = number_splited[0] + number_splited[1]
        obj.SN_number = number_splited[2]

    return obj

