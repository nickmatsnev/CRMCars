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
