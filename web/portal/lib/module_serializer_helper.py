from portal.serializers.module_serializer import ParserGetModuleSerializer, SourceGetModuleSerializer, \
    ScoringGetModuleSerializer, ParserModuleSerializer, SourceModuleSerializer, ScoringModuleSerializer


def get_read_serializer_by_module_type(module_type):
    if (module_type == "parser"):
        return ParserGetModuleSerializer
    if (module_type == "source"):
        return SourceGetModuleSerializer
    if (module_type == "scoring"):
        return ScoringGetModuleSerializer


def get_normal_serializer_by_module_type(module_type):
    if (module_type == "parser"):
        return ParserModuleSerializer
    if (module_type == "source"):
        return SourceModuleSerializer
    if (module_type == "scoring"):
        return ScoringModuleSerializer
