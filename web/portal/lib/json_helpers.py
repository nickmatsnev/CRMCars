


def build_sub_table(where,list_of_fields):
    table = {}
    for item in list_of_fields:
        table[item] = check_for_field(where,item)
    return table



def check_for_field(where,what):
    if where is not None:
        if where[what] is not None:
            return where[what]
        else:
            return ""
    else:
        return ""