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



#pathes

#work with INDIVIDUAL
URL_MAIN_INDIVIDUAL="/individual"
URL_MAIN_SUB_INDIVIDUAL_OPS= "/ops"
URL_MAIN_SUB_CUR_DATA= "/cur_gen/data"

URL_MODULE_SOURCE="source/"
URL_MODULE_SCORING="scoring/"
URL_MODULE_PARSER="parser/"

URL_INDIVIDUAL_METHOD_SCORE= "score/"
URL_INDIVIDUAL_METHOD_VALUES= "values/"

URL_INDIVIDUAL_METHOD_VALIDATE_ERRORS= "validate/errors/"
URL_INDIVIDUAL_METHOD_VALIDATE_STATUS= "validate/status/"
URL_INDIVIDUAL_METHOD_STOP_ERRORS= "stopfactor/errors/"
URL_INDIVIDUAL_METHOD_STOP_STATUS= "stopfactor/status/"

URL_INDIVIDUAL_OPS_POST_ACCEPT="postscoring_accept/"
URL_INDIVIDUAL_OPS_POST_REJECT="postscoring_reject/"
URL_INDIVIDUAL_OPS_PRE_REJECT="prescoring_reject/"
URL_INDIVIDUAL_OPS_GEN_NEXT="generation_next/"
URL_INDIVIDUAL_OPS_START="scoring_start/"

#work with MODULES
URL_MAIN_MODULE="/module"
URL_MODULE_METHOD_UPLOAD="upload/"
RESPONSE_ERROR = "Some error ;,,,((("

URL_MODULE_METHOD_VIEW_PARAMETERS="view/parameters/"
URL_MODULE_METHOD_VIEW="view/"

#work with CLIENT
URL_MAIN_CLIENT='/client'

URL_CLIENT_METHOD_VIEW='view/'
URL_CLIENT_METHOD_STATUS='status/'

URL_CLIENT_UPDATE_PRODUCT ='update_product/'

#work with PRODUCT
URL_MAIN_PRODUCT='/product'
URL_PRODUCT_METHOD_VIEW='view/'


#work with willz
URL_MAIN_WILLZ = '/willz'


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

