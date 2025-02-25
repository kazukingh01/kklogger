import time
from kklogger import set_logger

LOGGER = set_logger(__name__)
LOGGER.info("Hello, World!")
LOGGER.info("Hello, World!", color=["BOLD",      "GREEN"])
LOGGER.info("Hello, World!", color=["UNDERLINE", "BLUE"])
LOGGER.info("Hello, World!", color=["REVERCE",   "RED"])
LOGGER.info("Hello, World!", color=["INVISIBLE", "WHITE"])

LOGGER = set_logger(__name__, internal_log=True, is_force=True)
LOGGER.info("Hello, World!")
LOGGER.info("Hello, World!")
LOGGER.info("Hello, World!")
print(LOGGER.internal_stream.getvalue())

LOGGER = set_logger(__name__, logfilepath="test.log", is_force=True)
LOGGER.info("1")
LOGGER = set_logger(__name__, logfilepath="test.log", is_force=True, is_newlogfile=True)
LOGGER.info("2")
for _ in range(10):
    LOGGER = set_logger(__name__, logfilepath="test.%YYYY%-%MM%-%DD%-%hh%-%mm%-%ss%.log", is_force=True)
    LOGGER.info("3")
    time.sleep(1)
