# logging_config.py
import logging
import os
import settings

def setup_logging():
    level=settings.LOGGING_LEVEL  # Set to DEBUG or ERROR as needed
    level_int = logging.getLevelName(level)

    if len(logging.getLogger().handlers) > 0:
        # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
        # `.basicConfig` does not execute. Thus we set the level directly.
        logging.getLogger().setLevel(level_int)
    else:
        logging.basicConfig(level=level_int)