from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader


# this is special class to call method from python lib by name dynamically
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

    def get_parameters_meta(self):
        parameters = self.call_method("get_parameters_meta")['params']
        return parameters

    def get_source(self):
        return self.call_method("get_module_source")


class ParserModule(BasicModule):
    def __init__(self, module_path):
        super(ParserModule, self).__init__(module_path)
