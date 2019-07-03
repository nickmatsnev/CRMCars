# -*- coding: utf-8 -*-
# Exchanges
from os.path import expanduser

BASE_DATE = "01.01.1900"

MAIN_EXCHANGE_NAME = "main"

SOURCES_PROCESSOR_QUEUE = "sources_processor_queue"

# WILLZ_STATUS_UPDATER_QUEUE="willz_status_updater_queue"

PARSERS_PROCESSOR_QUEUE = "parsers_processor_queue"

CLIENT_PROCESSOR_QUEUE = "client_processor_queue"

SCORING_PROCESSOR_QUEUE = "scoring_processor_queue"

##Messages
CLIENT_RAW_CREATED_MESSAGE = "client_raw_created"

# CLIENT_PROCESSED_MESSAGE="client_processed"

# CLIENT_SCORING_COMPLETE_MESSAGE="client_scoring_complete"

INDIVIDUAL_PARSER_PROCESS_MESSAGE = "individual_parser_process"
INDIVIDUAL_PARSER_PROCESSED_MESSAGE = "individual_parser_processed"
INDIVIDUAL_PARSER_ERROR_MESSAGE = "individual_parser_error"

INDIVIDUAL_SCORING_PROCESS = "individual_scoring_process"
# INDIVIDUAL_SCORING_PROCESSED_MESSAGE="individiual_scoring_processed"

INDIVIDUAL_SOURCE_PROCESS_MESSAGE = "individual_process_source"
INDIVIDUAL_SOURCE_PROCESSED_MESSAGE = "individual_source_processed"
INDIVIDUAL_SOURCE_ERROR_MESSAGE = "individual_source_error"

CLIENT_PROCESSOR_NAME = "clientprocessor"
SCORING_PROCESSOR_NAME = "scoringprocessor"
PARSER_PROCESSOR_NAME = "parserprocessor"
SOURCE_PROCESSOR_NAME = "sourcesprocessor"

PATH_TO_SCORING_MODULES = "../../core/scoring/"
PATH_TO_PARSER_MODULES = "../../core/parsers/"
PATH_TO_SOURCE_MODULES = "../../core/sources/"

CLIENT_PROCESSOR_SUCCESS = " client is processed"
CLIENT_PROCESSOR_NOT_SUCCESS = " client is not processed"
CLIENT_PROCESSOR_WILLZ_SUCCESS = "Клиент загружен из системы WillZ"
CLIENT_PROCESSOR_MANUAL_SUCCESS = "Клиент создан в ручном режиме через портал"

PARSER_PROCESSOR_SUCCESS = "Обработаны данные от источника: "
PARSER_PROCESSOR_ERR_MODULE_NAME = 'Error: no module with requested name: '
PARSER_PROCESSOR_ERR_VALIDATION = 'Error: module has problem with validation: '
PARSER_PROCESSOR_ERR_STOP_FACTORS = 'Error: module has problem with stopfactors: '
PARSER_PROCESSOR_ERR_PARAMS = 'Error: module has problem with parameters: '
PARSER_PROCESSOR_UNKNOWN = 'Error: unknown '

SCORING_PROCESSOR_SCORING_START = "Начат процесс скоринга"
SCORING_PROCESSOR_SCORING_STOP = "Завершен процесс скоринга"
SCORING_PROCESSOR_PARSING_START = "Начат процесс парсинга источника"

SOURCE_PROCESSOR_USERNAME = "dmitry@korishchenko.ru"
SOURCE_PROCESSOR_TOKEN = "4def557c4fa35791f07cc8d4faf7c3a5f7ae7c93"
SOURCE_PROCESSOR_SOURCE_LOADED = "Загружен источник: "

SOURCE_PROCESSOR_ERR_MODULE_NAME = 'Error: no module with requested name: '
SOURCE_PROCESSOR_ERR_STRUCTURE = 'Error: module has problem with structure: '

RESPONSE_ERROR = "Some error ;,,,((("

# ********************** TEXT NAMES FOR URLS **************************

# names
NAME_API = "api"
NAME_SOURCE = "source"
NAME_SCORING = "scoring"
NAME_PARSER = "parser"
NAME_INDIVIDUAL = "individual"
NAME_OPS = "ops"
NAME_GENERATION = "generation"
NAME_DATA = "data"
NAME_SCORE = "score"
NAME_SSCORE = "Score"
NAME_VALUES = "values"
NAME_VVALUES = "Values"
NAME_VALIDATE = "validate"
NAME_VVALIDATE = "Validate"
NAME_STOPFACTOR = "stopfactor"
NAME_SSTOPFFACTORS = "StopFactors"
NAME_ERRORS = "errors"
NAME_STATUS = "status"
NAME_MODULE = "module"
NAME_UPLOAD = "upload"
NAME_VIEW = "view"
NAME_PARAMETERS = "parameters"
NAME_CLIENT = "client"
NAME_PRODUCT = "product"
NAME_WILLZ = "willz"
NAME_CONCRETE = "concrete"
NAME_USER = "user"
NAME_MESSAGE = "message"
NAME_CREDENTIALS = "credentials"
NAME_DELETE = "delete"
NAME_ACTIVATE = "activate"
NAME_DEACTIVATE = "deactivate"
NAME_FILTERED = "filtered"
NAME_INDEX = "index"
NAME_STATE = "state"
NAME_META = "meta"
NAME_ACCEPT = "accept"
NAME_REJECT = "reject"
NAME_INSPECT = "inspect"
NAME_LIST = "list"
NAME_REPORTS = "reports"
NAME_REPORT = "report"
NAME_START = "start"
NAME_DECLINE = "decline"
NAME_FORMS = "forms"
NAME_NEW = "new"
NAME_PROCESS = "process"
NAME_PROCESSOR = "processor"
NAME_BODY = "body"
NAME_UPDATE = "update"
NAME_GENERAL = "general"
NAME_ADVANCED = "advanced"
NAME_CACHE= "cache"


# specific names
NAME_HTML = ".html"
NAME_CUR_GEN = "cur_gen"
NAME_ADD_ACTION = "add_action"
NAME_BAD_REQUEST = "Bad request"
NAME_NO_CONTENT = "No content"
NAME_SCORING_COMPLETE_ACCEPTED_RU = "Одобрено после скоринга"
NAME_SCORING_RU = "Пользователь запустил процесс скоринга"
NAME_SCORING_COMPLETE_DECLINED_RU = "Отказано после скоринга"


#names with parameter used once
NAME_CURRENT_GENERATION = "current_" + NAME_GENERATION
NAME_POSTSCORING = "post" + NAME_SCORING
NAME_PRESCORING = "pre" + NAME_SCORING
NAME_INDIVIDUAL_OPERATIONS = NAME_INDIVIDUAL + "_operations"
NAME_GENERATION_NEXT = NAME_GENERATION + "_next"
NAME_GENERATIONS = NAME_GENERATION + "s"
NAME_PRODUCT_EDIT = NAME_PRODUCT + "_edit"
NAME_SCORING_CHECKS_FAILED = NAME_SCORING + "_checks_failed"
NAME_SCORING_COMPLETE = NAME_SCORING + "_complete"
NAME_MESSAGE_TYPE = NAME_MESSAGE + "_type"
NAME_MANUAL_DECLINE = "manual_" +NAME_DECLINE


#combined names
NAME_INDIVIDUAL_NEW_GENERATION = NAME_INDIVIDUAL + "_" + NAME_NEW + "_" + NAME_GENERATION
NAME_PRODUCT_NEW = NAME_PRODUCT + "_" + NAME_NEW
NAME_INDIVIDUAL_INSPECT = NAME_INDIVIDUAL + "_" + NAME_INSPECT
NAME_INDIVIDUAL_SCORING = NAME_INDIVIDUAL + "_" + NAME_SCORING
NAME_INDIVIDUAL_REPORT = NAME_INDIVIDUAL + "_" + NAME_REPORT
NAME_VALIDATE_STATUS = NAME_VALIDATE + "_" + NAME_STATUS
NAME_VALIDATE_ERRORS = NAME_VALIDATE + "_" + NAME_ERRORS
NAME_STOPFACTOR_STATUS = NAME_STOPFACTOR + "_" + NAME_STATUS
NAME_STOPFACTOR_ERRORS = NAME_STOPFACTOR + "_" + NAME_ERRORS
NAME_POSTSCORING_ACCEPT = NAME_POSTSCORING + "_" + NAME_ACCEPT
NAME_POSTSCORING_REJECT = NAME_POSTSCORING + "_" + NAME_REJECT
NAME_ACCEPT_INDIVIDUAL = NAME_ACCEPT + "_" + NAME_INDIVIDUAL
NAME_PRESCORING_REJECT = NAME_PRESCORING + "_" + NAME_REJECT
NAME_REJECT_INDIVIDUAL = NAME_REJECT + "_" + NAME_INDIVIDUAL
NAME_INDIVIDUAL_PRESCORING_DECLINE = NAME_INDIVIDUAL + "_" + NAME_PRESCORING + "_" + NAME_DECLINE
NAME_START_INDIVIDUAL_SCORING = NAME_START + "_" + NAME_INDIVIDUAL_SCORING
NAME_SCORING_START = NAME_SCORING + "_" + NAME_START
NAME_UPLOAD_FORMS = NAME_UPLOAD + "_" + NAME_FORMS
NAME_UPLOAD_MODULE = NAME_UPLOAD + "_" + NAME_MODULE
NAME_UPLOAD_CLIENT_MANUALLY = NAME_UPLOAD + "_" + NAME_CLIENT+ '_manually'
NAME_CLIENT_DECLINE = NAME_CLIENT + "_" + NAME_DECLINE
NAME_CLIENTS_LIST = NAME_CLIENT + "s_" + NAME_LIST
NAME_MODULES_LIST = NAME_MODULE + "s_" + NAME_LIST
NAME_PRODUCTS_LIST = NAME_PRODUCT + "s_" + NAME_LIST
NAME_USERS_LIST = NAME_USER + "s_" + NAME_LIST
NAME_SOURCES_PROCESSOR = NAME_SOURCE + "s_" + NAME_PROCESSOR
NAME_PARAMETERS_LIST = NAME_PARAMETERS + "_" + NAME_LIST
NAME_SCORING_PROCESSOR = NAME_SCORING + "_" + NAME_PROCESSOR
NAME_PARSERS_PROCESSOR = NAME_PARSER + "s_" + NAME_PROCESSOR
NAME_INDIVIDUAL_SCORING_PROCESS = NAME_INDIVIDUAL_SCORING + "_"+NAME_PROCESS
NAME_SCORING_COMPLETE_DECLINED = NAME_SCORING_COMPLETE + "_" + NAME_DECLINE + "d"
NAME_SCORING_COMPLETE_ACCEPTED = NAME_SCORING_COMPLETE + "_" + NAME_ACCEPT +"ed"
NAME_UPDATE_PRODUCT = NAME_UPDATE + "_" + NAME_PRODUCT


# ********************** CONVERTERS **************************

# pathes

# work with INDIVIDUAL
URL_MAIN_INDIVIDUAL = "/" + NAME_INDIVIDUAL + "/"
URL_MAIN_SUB_CUR_DATA = "/" + NAME_CUR_GEN + "/" + NAME_DATA + "/"

URL_MODULE_SOURCE = NAME_SOURCE + "/"
URL_MODULE_SCORING = NAME_SCORING + "/"
URL_MODULE_PARSER = NAME_PARSER + "/"

URL_INDIVIDUAL_METHOD_SCORE = NAME_SCORE + "/"
URL_INDIVIDUAL_METHOD_VALUES = NAME_VALUES + "/"

URL_INDIVIDUAL_METHOD_VALIDATE_ERRORS = NAME_VALIDATE + "/" + NAME_ERRORS + "/"
URL_INDIVIDUAL_METHOD_VALIDATE_STATUS = NAME_VALIDATE + "/" + NAME_STATUS + "/"
URL_INDIVIDUAL_METHOD_STOP_ERRORS = NAME_STOPFACTOR + "/" + NAME_ERRORS + "/"
URL_INDIVIDUAL_METHOD_STOP_STATUS = NAME_STOPFACTOR + "/" + NAME_STATUS + "/"

URL_INDIVIDUAL_OPS_POST_ACCEPT = "/" + NAME_OPS + "/" + NAME_POSTSCORING_ACCEPT + "/"
URL_INDIVIDUAL_OPS_POST_REJECT = "/" + NAME_OPS + "/" + NAME_POSTSCORING_REJECT + "/"
URL_INDIVIDUAL_OPS_PRE_REJECT = "/" + NAME_OPS + "/" + NAME_PRESCORING_REJECT + "/"
URL_INDIVIDUAL_OPS_GEN_NEXT = "/" + NAME_OPS + "/" + NAME_GENERATION_NEXT + "/"
URL_INDIVIDUAL_OPS_START = "/" + NAME_OPS + "/" + NAME_SCORING_START + "/"

# work with MODULES
URL_MAIN_MODULE = "/" + NAME_MODULE + "/"
URL_MODULE_METHOD_UPLOAD = "/" + NAME_UPLOAD + "/"

URL_MODULE_METHOD_VIEW_PARAMETERS = NAME_VIEW + "/" + NAME_PARAMETERS + "/"
URL_MODULE_METHOD_VIEW = NAME_VIEW + "/"

# work with CLIENT
URL_MAIN_CLIENT = '/' + NAME_CLIENT + '/'

URL_CLIENT_METHOD_VIEW = '/' + NAME_VIEW + '/'
URL_CLIENT_METHOD_STATUS = NAME_STATUS + '/'

URL_CLIENT_UPDATE_PRODUCT = NAME_UPDATE_PRODUCT + '/'

# work with PRODUCT
URL_MAIN_PRODUCT = '/' + NAME_PRODUCT + '/'
URL_PRODUCT_METHOD_VIEW = NAME_VIEW + '/'

# work with willz
URL_MAIN_WILLZ = '/' + NAME_WILLZ + '/'

# work with VIEW


URL_LINK_INDIVIDUAL_SCORING = NAME_CONCRETE + "/" + NAME_INDIVIDUAL_SCORING + NAME_HTML
URL_LINK_INDIVIDUAL_REPORT = NAME_CONCRETE + "/" + NAME_INDIVIDUAL_REPORT + NAME_HTML
URL_LINK_INDIVIDUAL_INSPECT = NAME_CONCRETE + "/" + NAME_INDIVIDUAL_INSPECT + NAME_HTML
URL_LINK_INDIVIDUAL_OPERATIONS = NAME_CONCRETE + "/" + NAME_INDIVIDUAL_OPERATIONS + NAME_HTML

URL_LINK_CLIENT_DECLINE = NAME_CONCRETE + "/" + NAME_CLIENT_DECLINE + NAME_HTML
URL_LINK_UPLOAD_MODULE = NAME_CONCRETE + "/" + NAME_FORMS + "/" + NAME_UPLOAD_MODULE + NAME_HTML
URL_LINK_PRODUCT_EDIT = NAME_CONCRETE + "/" + NAME_FORMS + "/" + NAME_PRODUCT_EDIT + NAME_HTML
URL_LINK_SOURCE = NAME_CONCRETE + "/" + NAME_SOURCE + NAME_HTML
URL_LINK_REPORTS = NAME_CONCRETE + "/" + NAME_REPORTS + NAME_HTML
URL_LINK_INDEX = NAME_INDEX + NAME_HTML

URL_LINK_PARAMETERS_LIST = NAME_CONCRETE + "/" + NAME_PARAMETERS_LIST + NAME_HTML
URL_LINK_PRODUCTS_LIST = NAME_CONCRETE + "/" + NAME_PRODUCTS_LIST + NAME_HTML
URL_LINK_MODULES_LIST = NAME_CONCRETE + "/" + NAME_MODULES_LIST + NAME_HTML
URL_LINK_CLIENTS_LIST = NAME_CONCRETE + "/" + NAME_CLIENTS_LIST + NAME_HTML
URL_LINK_USERS_LIST = NAME_CONCRETE + "/" + NAME_USERS_LIST + NAME_HTML

MODULE_DICTIONARY = {"source": "Источников", "parser": "Парсеров", "scoring": "Скоринга"}

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Russia+2019!"

home = expanduser("~")

LOG_FILE_FORMAT_STRING = home + "/.log/{0}.log"
