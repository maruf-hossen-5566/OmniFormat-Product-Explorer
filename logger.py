import logging
from logging.handlers import RotatingFileHandler
import os

# Streamlit Cloud-safe directory
LOG_DIR = os.getenv("LOG_DIR", "/tmp/logs")
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))  # Default INFO for production

    formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
    )

    # 1️⃣ Console handler (Streamlit Cloud captures this)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2️⃣ File handler (only if filesystem is writable)
    try:
        file_handler = RotatingFileHandler(
            f"{LOG_DIR}/app.log",
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        # If file can't be created (rare), continue gracefully
        pass

    return logger
