

from loguru import logger
import sys
import json
from typing import Any, Dict, Optional

class LoggerService:
    def __init__(self, service: str ):

        self.logger = logger
        self.service = service

        # Remove default handlers to avoid duplicate logs
        logger.remove()
        # Add a console handler
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO",
            enqueue=False,
            backtrace=True,
            diagnose=True
        )

        logger.add(
            "logs/app.json",
            level="INFO",
            rotation="5 MB",       
            retention="10 days",   
            compression="zip",     # compress old files
            serialize=True         
        )


    def log(self, level: str, message: str, data: Optional[Dict[str, Any]] = None):
      
        log_entry = {"message": message, "service": self.service}
        if data:
            log_entry["data"] = data

        # Convert to JSON for consistency
        log_text = json.dumps(log_entry, default=str)

        # Route to correct log level
        level = level.lower()
        if level == "info":
            self.logger.info(log_text)
        elif level == "warning":
            self.logger.warning(log_text)
        elif level == "error":
            self.logger.error(log_text)
        elif level == "debug":
            self.logger.debug(log_text)
        else:
            self.logger.info(log_text)

      
