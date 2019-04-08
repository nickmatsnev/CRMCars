#Exchanges
MAIN_EXCHANGE_NAME="main"

SOURCES_PROCESSOR_QUEUE = "sources_processor_queue"

# WILLZ_STATUS_UPDATER_QUEUE="willz_status_updater_queue"

PARSERS_PROCESSOR_QUEUE = "parsers_processor_queue"

CLIENT_PROCESSOR_QUEUE="client_processor_queue"

SCORING_PROCESSOR_QUEUE="scoring_processor_queue"



##Messages
CLIENT_RAW_CREATED_MESSAGE="client_raw_created"

# CLIENT_PROCESSED_MESSAGE="client_processed"

# CLIENT_SCORING_COMPLETE_MESSAGE="client_scoring_complete"

INDIVIDUAL_PARSER_PROCESS_MESSAGE = "individual_parser_process"
INDIVIDUAL_PARSER_PROCESSED_MESSAGE = "individual_parser_processed"
INDIVIDUAL_PARSER_ERROR_MESSAGE = "individual_parser_error"

INDIVIDUAL_SCORING_PROCESS="individual_scoring_process"
# INDIVIDUAL_SCORING_PROCESSED_MESSAGE="individiual_scoring_processed"

INDIVIDUAL_SOURCE_PROCESS_MESSAGE = "individual_process_source"
INDIVIDUAL_SOURCE_PROCESSED_MESSAGE = "individual_source_processed"
INDIVIDUAL_SOURCE_ERROR_MESSAGE = "individual_source_error"

CLIENT_PROCESSOR_NAME = "New Client Processor"

PATH_TO_SCORING_MODULES = "../../core/scoring/"
PATH_TO_PARSER_MODULES = "../../core/parsers/"
PATH_TO_SOURCE_MODULES = "../../core/sources/"


CLIENT_PROCESSOR_SUCCESS = " client is processed"
CLIENT_PROCESSOR_NOT_SUCCESS = " client is not processed"
CLIENT_PROCESSOR_WILLZ_SUCCESS = "Клиент загружен из системы WillZ"


PARSER_PROCESSOR_SUCCESS  = "Обработаны данные от источника: "
PARSER_PROCESSOR_ERR_MODULE_NAME  = 'Error: no module with requested name: '
PARSER_PROCESSOR_ERR_VALIDATION  = 'Error: module has problem with validation: '
PARSER_PROCESSOR_ERR_STOP_FACTORS  = 'Error: module has problem with stopfactors: '
PARSER_PROCESSOR_ERR_PARAMS  = 'Error: module has problem with parameters: '
PARSER_PROCESSOR_UNKNOWN = 'Error: unknown '


SCORING_PROCESSOR_SCORING_START = "Начат процесс скоринга"
SCORING_PROCESSOR_SCORING_STOP = "Завершен процесс скоринга"
SCORING_PROCESSOR_PARSING_START = "Начат процесс парсинга источника"

SOURCE_PROCESSOR_USERNAME = "dmitry@korishchenko.ru"
SOURCE_PROCESSOR_TOKEN = "4def557c4fa35791f07cc8d4faf7c3a5f7ae7c93"
SOURCE_PROCESSOR_SOURCE_LOADED = "Загружен источник: "

SOURCE_PROCESSOR_ERR_MODULE_NAME  = 'Error: no module with requested name: '
SOURCE_PROCESSOR_ERR_STRUCTURE  = 'Error: module has problem with structure: '

RESPONSE_ERROR = "Some error ;,,,((("

#********************** TEXT NAMES FOR URLS **************************

#names
NAME_SOURCE = "source"
NAME_SCORING = "scoring"
NAME_PARSER = "parser"
NAME_INDIVIDUAL = "individual"
NAME_OPS = "ops"
NAME_CUR_GEN = "cur_gen"
NAME_DATA = "data"
NAME_POSTSCORING_ACCEPT = "postscoring_accept"
NAME_POSTSCORING_REJECT = "postscoring_reject"
NAME_PRESCORING_REJECT = "prescoring_reject"
NAME_GENERATION_NEXT = "generation_next"
NAME_SCORING_START = "scoring_start"
NAME_SCORE  = "score"
NAME_VALUES = "values"
NAME_VALIDATE = "validate"
NAME_STOPFACTOR = "stopfactor"
NAME_ERRORS = "errors"
NAME_STATUS = "status"
NAME_MODULE = "module"
NAME_UPLOAD = "upload"
NAME_VIEW = "view"
NAME_PARAMETERS = "parameters"
NAME_CLIENT = "client"
NAME_PRODUCT = "product"
NAME_UPDATE_PRODUCT = "update_product"
NAME_WILLZ = "willz"

#********************** CONVERTERS **************************

#pathes

#work with INDIVIDUAL
URL_MAIN_INDIVIDUAL="/" + NAME_INDIVIDUAL + "/"
URL_MAIN_SUB_CUR_DATA= "/" + NAME_CUR_GEN + "/" + NAME_DATA + "/"

URL_MODULE_SOURCE=NAME_SOURCE+"/"
URL_MODULE_SCORING=NAME_SCORING+"/"
URL_MODULE_PARSER=NAME_PARSER+"/"

URL_INDIVIDUAL_METHOD_SCORE= NAME_SCORE + "/"
URL_INDIVIDUAL_METHOD_VALUES= NAME_VALUES + "/"

URL_INDIVIDUAL_METHOD_VALIDATE_ERRORS= NAME_VALIDATE + "/" + NAME_ERRORS + "/"
URL_INDIVIDUAL_METHOD_VALIDATE_STATUS= NAME_VALIDATE + "/" + NAME_STATUS + "/"
URL_INDIVIDUAL_METHOD_STOP_ERRORS= NAME_STOPFACTOR + "/" + NAME_ERRORS + "/"
URL_INDIVIDUAL_METHOD_STOP_STATUS= NAME_STOPFACTOR + "/" + NAME_STATUS + "/"

URL_INDIVIDUAL_OPS_POST_ACCEPT= "/" + NAME_OPS + "/" + NAME_POSTSCORING_ACCEPT + "/"
URL_INDIVIDUAL_OPS_POST_REJECT="/" + NAME_OPS + "/" + NAME_POSTSCORING_REJECT + "/"
URL_INDIVIDUAL_OPS_PRE_REJECT="/" + NAME_OPS + "/" + NAME_PRESCORING_REJECT + "/"
URL_INDIVIDUAL_OPS_GEN_NEXT="/" + NAME_OPS + "/" + NAME_GENERATION_NEXT + "/"
URL_INDIVIDUAL_OPS_START="/" + NAME_OPS + "/" + NAME_SCORING_START + "/"

#work with MODULES
URL_MAIN_MODULE="/" + NAME_MODULE + "/"
URL_MODULE_METHOD_UPLOAD= "/" + NAME_UPLOAD + "/"

URL_MODULE_METHOD_VIEW_PARAMETERS=NAME_VIEW  + "/" + NAME_PARAMETERS + "/"
URL_MODULE_METHOD_VIEW=NAME_VIEW + "/"

#work with CLIENT
URL_MAIN_CLIENT='/' + NAME_CLIENT + '/'

URL_CLIENT_METHOD_VIEW='/' + NAME_VIEW + '/'
URL_CLIENT_METHOD_STATUS=NAME_STATUS + '/'

URL_CLIENT_UPDATE_PRODUCT =NAME_UPDATE_PRODUCT + '/'

#work with PRODUCT
URL_MAIN_PRODUCT='/' + NAME_PRODUCT + '/'
URL_PRODUCT_METHOD_VIEW=NAME_VIEW + '/'


#work with willz
URL_MAIN_WILLZ = '/' + NAME_WILLZ + '/'


#work with VIEW

URL_INDIVIDUAL_INSPECT="individual_inspect"
URL_CLIENTS_LIST="clients_list"
URL_MODULES_LIST="modules_list"
URL_PRODUCTS_LIST="products_list"
URL_REPORTS="reports"

URL_LINK_INDIVIDUAL_SCORING="concrete/individual_scoring.html"
URL_LINK_INDIVIDUAL_INSPECT="concrete/individual_inspect.html"
URL_LINK_INDIVIDUAL_OPERATIONS="concrete/individual_operations.html"

URL_LINK_CLIENT_DECLINE="concrete/client_decline.html"
URL_LINK_UPLOAD_MODULE="concrete/forms/upload_module.html"
URL_LINK_PRODUCT_EDIT="concrete/forms/product_edit.html"
URL_LINK_SOURCE="concrete/source.html"
URL_LINK_REPORTS="concrete/reports.html"
URL_LINK_INDEX="index.html"

URL_LINK_PARAMETERS_LIST="concrete/parameters_list.html"
URL_LINK_PRODUCTS_LIST="concrete/products_list.html"
URL_LINK_MODULES_LIST="concrete/modules_list.html"
URL_LINK_CLIENTS_LIST="concrete/clients_list.html"
URL_LINK_USERS_LIST="concrete/users_list.html"

