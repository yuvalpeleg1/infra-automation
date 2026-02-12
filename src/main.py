import sys
import logging

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s\t%(filename)s - %(funcName)s - %(message)s"
)
print_handler = logging.StreamHandler(sys.stdout)
print_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/my.log")
print_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(print_handler)
    logger.addHandler(file_handler)

logger.error("Check Error")
