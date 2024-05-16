import logging
from logging.handlers import TimedRotatingFileHandler

import time
from datetime import datetime
import os
import traceback


def init_logger(base_file="log"):

    file_format_date = time.strftime("%Y%m%d", time.localtime(time.time()))
    log_dir = os.path.dirname("./logs/")

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, base_file + file_format_date + ".log")

    fileHandler = TimedRotatingFileHandler(
        filename=log_file, when="D", interval=1, encoding="utf-8"
    )

    BASIC_FORMAT = "%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s"
    formatter = logging.Formatter(BASIC_FORMAT)
    fileHandler.setFormatter(formatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel("INFO") 

    # logging.basicConfig(level=logging.INFO, format=formatter)
    _logger = logging.getLogger()
    _logger.handlers.clear()
    _logger.addHandler(fileHandler)
    _logger.addHandler(consoleHandler)
    _logger.setLevel(logging.INFO)

    _logger.info(f"{base_file} logger init success")

    yield _logger
    _logger.info("logger yield success")
    return _logger


logger = init_logger().__next__()
