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

INDIVIDUAL_PARSERS_PROCESS_MESSAGE = "individual_parsers_processed"
INDIVIDUAL_PARSERS_PROCESSED_MESSAGE = "individual_parsers_processed"

INDIVIDUAL_SCORING_PROCESS="individual_scoring_process"
# INDIVIDUAL_SCORING_PROCESSED_MESSAGE="individiual_scoring_processed"

INDIVIDUAL_SOURCES_PROCESS_MESSAGE = "individual_process_sources"
INDIVIDUAL_SOURCES_PROCESSED_MESSAGE = "individual_sources_processed"


CLIENT_PROCESSOR_NAME = "New Client Processor"

PATH_TO_SCORING_MODULES = "../../core/scoring/"
PATH_TO_PARSER_MODULES = "../../core/parsers/"
PATH_TO_SOURCE_MODULES = "../../core/sources/"
