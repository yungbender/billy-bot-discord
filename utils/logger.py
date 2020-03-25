import logging
import colorlog

LOGGER = logging.getLogger("billy-logger")

FORMATTER = colorlog.ColoredFormatter("%(filename)s.%(funcName)s@%(asctime)s : %(levelname)s - %(message)s", 
                                      log_colors=
                                      {
                                          "DEBUG": "cyan",
                                          "INFO": "green",
                                          "WARNING": "yellow",
                                          "ERROR": "red",
                                          "CRITICAL": "red",
                                      })
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

FILE_HANDLER = logging.FileHandler("billy.log")
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILE_HANDLER)

LOGGER.setLevel(logging.INFO)
