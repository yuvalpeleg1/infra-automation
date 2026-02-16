import logging
from pathlib import Path

# logs file path
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "provisioning.log"

# Setting up the logger
def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s\t%(filename)s - %(funcName)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
