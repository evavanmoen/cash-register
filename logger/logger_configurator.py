import sys
import logging


def get_logger(name):
    """This function collecting all the logs and saving them in the desired file (in this case called
    'cash_register_debug.log')
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/cash_register_debug.log")
        ]
    )

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger(name)

    return logger
