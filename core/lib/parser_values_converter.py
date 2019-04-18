def get_parser_values(parsers_values):
    parsers_list = {}
    for parser_name in parsers_values:
        items_list = {}
        for item in parsers_values[parser_name]:
            items_list[item['name']] = item['value']
        parsers_list[parser_name] = items_list
    return parsers_list
