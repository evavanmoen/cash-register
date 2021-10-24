import sys
import json

import constants.constants as const
import logger.logger_configurator as logger_configurator

logger = logger_configurator.get_logger(__name__)


def products_check(dict_products):
    """This function verifies that the length of the dictionary values is the same"""

    len_aux = 0

    # If the json file is empty returns unstable code
    if not dict_products:
        logger.error("The json file is empty")
        sys.exit(const.EXIT_CODE_UNSTABLE)

    # Or is not empty see the lengths for values
    else:
        # check values length
        for value in dict_products.values():
            len_value = len(value)
            if len_aux == 0:
                len_aux = len_value
            else:
                if len_aux != len_value:
                    logger.info("The json file is not correct by lengths for values")
                    sys.exit(const.EXIT_CODE_BAD)

        # check existing keys at this moment
        if not all(item in list(dict_products.keys()) for item in const.PRODUCTS_COLUMNS):
            logger.error("The json file is not correct by columns")
            sys.exit(const.EXIT_CODE_BAD)


def exists_products():
    """This function read json configuration with exists products (code, name and price) and created
    dictionaries for this information
    """

    # Path of json configuration
    json_path = const.PATH_JSON_CASH_REGISTER
    logger.info("Reading json file: {}".format(json_path))

    # Get information the exists products
    try:
        json_data = open(json_path)
        dict_products = json.load(json_data)
        json_data.close()
    except Exception as ex:
        logger.error("Error load configuration file: {}".format(ex))
        sys.exit(const.EXIT_CODE_BAD)

    products_check(dict_products)
    logger.info("Catalog: {}".format(dict_products))

    return dict_products


def main():
    products = exists_products()
    sys.exit(const.EXIT_CODE_OK)


if __name__ == "__main__":
    main()
