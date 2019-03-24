from lib import basic_api_requestor
from lib.modules import ScoringModule, ParserModule, SourceModule


def get_sources_deps(scoring_module_id):
    scoring_m = get_scoring_module(scoring_module_id)

    deps = scoring_m.get_dependencies()

    parser_modules = []
    for dep in deps:
        parser_modules.append(dep)
    parser_modules_deps = list(set(parser_modules))  # unique list

    source_modules = []
    for parser in parser_modules_deps:
        parser = basic_api_requestor.request('/module/parser/{0}/'.format(parser))[0]
        parser_m = ParserModule(parser['path'])
        source_modules.append(parser_m.get_module_source())
    return source_modules


def get_parser_deps(product_id):
    scoring_m = get_scoring_module(product_id)

    deps = scoring_m.get_dependencies()
    parser_modules = []
    for dep in deps:
        parser_modules.append(dep)
    return list(set(parser_modules))  # unique list


def get_scoring_module(primary_scoring_module_id):
    primary_scoring = basic_api_requestor.request('/module/scoring/{0}/'.format(primary_scoring_module_id))
    return ScoringModule(primary_scoring['path'])
