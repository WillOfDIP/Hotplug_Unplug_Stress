# ta_rtl_lib.py


"""
Python Run Time Logger.
Utilizes standard logging package for Python.
TODO: Add short description what it does.
To use:
1. In the 'main' script:
1.1. Setup logger by calling logger_setup at the beginning.
Note: Not required if the 'main' script framed by 
script execution context manager (see ta_flow_frame_lib).
1.2. Get logger to log messages by calling get_logger.
1.3. Shutdown logger by calling shutdown at the end.
Note: Not required if the 'main' script framed by 
script execution context manager (see ta_flow_frame_lib) and
script finished with sys.exit() call.
2. In each module:
2.1. Get logger to log messages by calling get_logger 
at the beginning of the module.
"""


import logging
import logging.config


# Globals:
LOGGER_NAME = 'ta_rtl'


def logger_setup(strLogsBaseName=None, dictLoggerConfig=None):
    """Sets up current script root logger named ta_rtl.
    Input parameters:
    1. strLogsBaseName - base name for logs:
    strLogsBaseName_dbg.log - debug messages.
    strLogsBaseName_info.log - info messages.
    strLogsBaseName_wrn.log - warning messages.
    If None:
    script
    2. dictLoggerConfig - alternative root logger configuration
    as a dictionary if specified.
    Current limitation: root logger name has to be ta_rtl.
    """

    # TODO: Add sanity checks for input parameters

    # Defaults:
    strLoggerNameDflt = LOGGER_NAME
    strLogsBaseNameDflt = 'script'
    strLogsExtDflt = '.log'

    # Update Default Logging Configuration if needed
    strLoggerName = strLoggerNameDflt

    if strLogsBaseName is None:
        strLogsBaseName = strLogsBaseNameDflt

    strLogsExt = strLogsExtDflt

    dictLoggerConfigDflt = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s: %(name)s: %(levelname)s: %(funcName)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
            },
            'file_dbg': {
                'class': 'logging.FileHandler',
                'filename': strLogsBaseName + '_dbg' + strLogsExt,
                'level': 'DEBUG',
                'formatter': 'default',
            },
            'file_info': {
                'class': 'logging.FileHandler',
                'filename': strLogsBaseName + '_info' + strLogsExt,
                'level': 'INFO',
                'formatter': 'default',
            },
            'file_wrn': {
                'class': 'logging.FileHandler',
                'filename': strLogsBaseName + '_wrn' + strLogsExt,
                'level': 'WARNING',
                'formatter': 'default',
            },
        },
        'loggers': {
            strLoggerName: {
                'handlers':['console', 'file_dbg', 'file_info', 'file_wrn'],
                'level':'DEBUG',
            },
        }
    }

    # Configure Logger
    if dictLoggerConfig is None:
        logging.config.dictConfig(dictLoggerConfigDflt)
    else:
        logging.config.dictConfig(dictLoggerConfig)

    # Redirect warnings issued by the warnings module to the logging system
    logging.captureWarnings(True)



def get_logger(strLoggerName=None):
    """Instantiates logger.
    
    
    Input parameter:
    strLoggerName:
    Name of the root logger child.
    Returns:
    
    Instance of the logger named ta_rtl.strLoggerName
    if strLoggerName specified or
    Instance of the root logger ta_rtl otherwise.
    """

    if strLoggerName is None:
        strLoggerName = LOGGER_NAME
    else:
        strLoggerName = LOGGER_NAME +'.' + strLoggerName.strip() 

    return logging.getLogger(strLoggerName)


def logger_shutdown():
    """Requests logger orderly shutdown."""
    logging.shutdown()