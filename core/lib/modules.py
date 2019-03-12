import sys

sys.path.append('../')
sys.path.append('../../')
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
from core.lib.constants import *

# this is special class to call method from python lib by name dynamically
#from portal.serializers.backend import ParserModuleSerializer, SourceModuleSerializer, ScoringModuleSerializer, \
#    ParserGetModuleSerializer, SourceGetModuleSerializer, ScoringGetModuleSerializer


class BasicModule:

    # dynamically loads method from proposed absolute path (to .py file)
    def __init__(self, module_path):
        loader = SourceFileLoader('', module_path)
        spec = spec_from_loader(loader.name, loader)
        self.__mod = module_from_spec(spec)
        loader.exec_module(self.__mod)

    # dynamically call method with concrete name and parameters
    def call_method(self, method_name, **parameters):
        func = getattr(self.__mod, method_name)
        return func(**parameters)

    def get_module_name(self):
        return self.call_method("get_module_name")


class ParserModule(BasicModule):
    def __init__(self, module_path):
        super(ParserModule, self).__init__(module_path)

    def get_available_parameters(self):
        parameters = self.call_method("get_available_params")
        return parameters

    def get_module_source(self):
        return self.call_method("get_module_source")

    def get_values(self, source_json):
        return self.call_method("get_values", source_json=source_json)

    def validate(self, individual_json, source_json):
        return self.call_method("validate", individual_json=individual_json, source_json=source_json)

    def stop_factors(self, individual_json, source_json):
        return self.call_method("stop_factors", individual_json=individual_json, source_json=source_json)


class SourceModule(BasicModule):
    def __init__(self, module_path):
        super(SourceModule, self).__init__(module_path)

    def get_module_url(self):
        return self.call_method("get_module_url")

    def import_data(self, credentials_json, individual_json):
        return self.call_method("import_data", credentials_json=credentials_json, individual_json=individual_json)


class ScoringModule(BasicModule):
    def __init__(self, module_path):
        super(ScoringModule, self).__init__(module_path)

    def get_score(self, parsers_data):
        return self.call_method("get_score", parsers_data=parsers_data)

    def get_dependencies(self):
        return self.call_method("get_dependencies")



def get_class_by_module_type(module_type):
    if (module_type == "parser"):
        return ParserModule
    if (module_type == "source"):
        return SourceModule
    if (module_type == "scoring"):
        return ScoringModule


def get_subtype_by_module_type(module_type):
    if (module_type == "parser"):
        return "parser"
    if (module_type == "source"):
        return "source"
    if (module_type == "scoring"):
        return "scoring"


def get_path_by_module_type(module_type):
    if (module_type == "parser"):
        return PATH_TO_PARSER_MODULES
    if (module_type ==  "source"):
        return PATH_TO_SOURCE_MODULES
    if (module_type == "scoring"):
        return PATH_TO_SCORING_MODULES