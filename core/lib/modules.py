from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

# this is special class to call method from python lib by name dynamically
from portal.serializers.backend import ParserModuleSerializer, SourceModuleSerializer, ScoringModuleSerializer, \
    ParserGetModuleSerializer, SourceGetModuleSerializer, ScoringGetModuleSerializer


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
        parameters = self.call_method("get_available_params")['params']
        return parameters

    def get_source(self):
        return self.call_method("get_module_source")

    def get_values(self, raw_data):
        return self.call_method("get_values", raw_data)

    def validate(self, raw_data, client):
        return self.call_method("validate", raw_data, client)


class SourceModule(BasicModule):
    def __init__(self, module_path):
        super(SourceModule, self).__init__(module_path)

    def get_module_url(self):
        return self.call_method("get_module_url")

    def import_data(self, credentials, client):
        return self.call_method("import_data")


class ScoringModule(BasicModule):
    def __init__(self, module_path):
        super(ScoringModule, self).__init__(module_path)


def get_subtype_by_module_type(module_type):
    if (module_type == ParserModule):
        return "Parser";
    if (module_type == SourceModule):
        return "Source";
    if (module_type == ScoringModule):
        return "Scoring";


def get_read_serializer_by_module_type(module_type):
    if (module_type == ParserModule):
        return ParserGetModuleSerializer;
    if (module_type == SourceModule):
        return SourceGetModuleSerializer;
    if (module_type == ScoringModule):
        return ScoringGetModuleSerializer;


def get_normal_serializer_by_module_type(module_type):
    if (module_type == ParserModule):
        return ParserModuleSerializer;
    if (module_type == SourceModule):
        return SourceModuleSerializer;
    if (module_type == ScoringModule):
        return ScoringModuleSerializer;
