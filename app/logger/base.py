import logging

FORMAT = "%(asctime)s | %(levelname)8s | %(name)27s | %(message)s"

GREY = "\x1b[0;37m"
LIGHT_GREY = "\x1b[0;36m"
BLUE = "\x1b[0;34m"
YELLOW = "\x1b[0;32m"
RED = "\x1b[0;31m"
BOLD_RED = "\x1b[1;31m"
RESET = "\x1b[0m"

FORMATS = {
    logging.DEBUG: GREY + FORMAT + RESET,
    logging.INFO: BLUE + FORMAT + RESET,
    logging.WARNING: YELLOW + FORMAT + RESET,
    logging.ERROR: RED + FORMAT + RESET,
    logging.CRITICAL: BOLD_RED + FORMAT + RESET,
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # level of logger in console
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    return logger
