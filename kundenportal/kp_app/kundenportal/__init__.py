from sys import stderr
from logging import FileHandler, getLogger, StreamHandler, DEBUG, Formatter, INFO
LOGGER = getLogger(__name__)
LOGGER.setLevel(DEBUG)
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler = StreamHandler(stderr)
stream_handler.setLevel(DEBUG)
stream_handler.setFormatter(formatter)
file_handler = FileHandler("kundenportal.log")
file_handler.setLevel(INFO)
file_handler.setFormatter(formatter)
LOGGER.addHandler(stream_handler)
LOGGER.addHandler(file_handler)

LOGGER.info("Starting kundenportal")
