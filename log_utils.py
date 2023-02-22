import logging

logging.basicConfig(filemode='w')


def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f'logs/{name}.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler_format = logging.Formatter(
        fmt='[%(asctime)s] - %(levelname)s - %(name)s:%(funcName)s - %(message)s')
    file_handler.setFormatter(file_handler_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler_format = logging.Formatter(fmt='%(levelname)s:: %(message)s')
    console_handler.setFormatter(console_handler_format)

    root_file_handler = logging.FileHandler(f'logs/discussion-platform.log', mode='w')
    root_file_handler.setFormatter(file_handler_format)
    root_file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(root_file_handler)
