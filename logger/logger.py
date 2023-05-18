import logging
import os

directory = "logs"

if not os.path.exists(directory):
    os.makedirs(directory)

def log(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s: %(levelname)s: %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    file_handler = logging.FileHandler('logs/app.log', mode='a')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
