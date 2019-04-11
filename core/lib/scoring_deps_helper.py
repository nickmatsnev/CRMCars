
from lib.modules import ScoringModule, ParserModule, SourceModule


def get_sources_deps(api_requestor, scoring_module_id):
    scoring_m = get_scoring_module(api_requestor, scoring_module_id)

    deps = scoring_m.get_dependencies()

    parser_modules = []
    for dep in deps:
        parser_modules.append(dep)
    parser_modules_deps = list(set(parser_modules))  # unique list

    source_modules = []
    for parser in parser_modules_deps:
        parser = api_requestor.get_parser_module_by_name(parser)
        parser_m = ParserModule(parser['path'])
        source_modules.append(parser_m.get_module_source())
    return source_modules


def get_parser_deps(api_requestor, scoring_module_id):
    scoring_m = get_scoring_module(api_requestor, scoring_module_id)

    deps = scoring_m.get_dependencies()
    parser_modules = []
    for dep in deps:
        parser_modules.append(dep)
    return list(set(parser_modules))  # unique list


def get_scoring_module(api_requestor, primary_scoring_module_id):
    primary_scoring = api_requestor.get_scoring_module_by_name(primary_scoring_module_id)
    return ScoringModule(primary_scoring['path'])
