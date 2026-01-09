# import logging
# import logging.config

# LOG_FORMAT = (
#     "%(asctime)s | %(levelname)s | %(name)s | "
#     "%(filename)s:%(lineno)d | %(message)s"
# )

# LOGGING_CONFIG = {
#     "version": 1,
#     "disable_existing_loggers": False,

#     "formatters": {
#         "default": {
#             "format": LOG_FORMAT
#         },
#     },

#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "default",
#         },
#         "file": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/app.log",
#             "maxBytes": 10_000_000,
#             "backupCount": 5,
#             "formatter": "default",
#         },
#     },

#     "root": {
#         "level": "INFO",
#         "handlers": ["console", "file"],
#     },
# }

# def setup_logging():
#     logging.config.dictConfig(LOGGING_CONFIG)

# logger_config.py
from loguru import logger
import sys

# Remove default logger (optional)
logger.remove()

# Console logs
logger.add(
    sys.stdout, 
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
)


logger.add(
    "logs/app.json",
    level="DEBUG",
    rotation="5 MB",       
    retention="10 days",   
    compression="zip",     # compress old files
    serialize=True         
)


logger.add(
    "logs/error.log",
    level="ERROR",
    filter=lambda record: record["level"].name == "ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


