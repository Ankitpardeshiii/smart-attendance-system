#!/usr/bin/env python3
"""
Logging Wrapper for Advanced Face Detection System
This wraps your existing test script WITHOUT modifying it.
"""

import logging
import logging.handlers
import sys
import os
from datetime import datetime


# ==============================
# LOGGING CONFIGURATION
# ==============================

def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(
        log_dir,
        f"system_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File Handler (Rotating)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("============================================")
    logger.info("Advanced Face Detection System Test Started")
    logger.info("============================================")
    logger.info(f"Log file created at: {log_file}")

    return logger


# ==============================
# Redirect print() to logging
# ==============================

class PrintLogger:
    """
    Redirects print statements to logging system.
    """

    def write(self, message):
        if message.strip() != "":
            logging.info(message.strip())

    def flush(self):
        pass


# ==============================
# MAIN EXECUTION WRAPPER
# ==============================

def main():
    setup_logging()

    # Redirect stdout and stderr
    sys.stdout = PrintLogger()
    sys.stderr = PrintLogger()

    try:
        # Import your original script
        import test  # <-- replace with your actual script filename (without .py)

        # Run its main()
        if hasattr(test, "main"):
            test.main()

        logging.info("System test completed successfully.")

    except Exception as e:
        logging.exception("Critical error occurred while running test script")


if __name__ == "__main__":
    main()