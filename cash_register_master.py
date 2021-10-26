import sys
import json

import constants.constants as const
import logger.logger_configurator as logger_configurator

logger = logger_configurator.get_logger(__name__)


def scan(code, products):
    """This function gets code to scan and add 1 unit in field units in the correspondent dictionary
    :param code: product code name
    :param products: list with exists products
    """

    for p in products:
        if p[const.PRODUCTS_CODE] == code:
            p[const.PRODUCTS_UNITS] = p[const.PRODUCTS_UNITS] + 1


def bulk_discount(code, units, price, discounts):
    """This function collects the bulk discount that is requested for a specific product
    (for example, 3 or more TSHIRT items, the price per unit should be 19.00€)
    :param code: product code name
    :param units: units mark at discount
    :param price: new item price
    :param discounts: discounts list
    """

    # If the code is existing and the unit and price are positive values
    if len(code) > 0 and units > 0 and price > 0.0:

        # created the new discount
        dict_bulk_discount = {
            const.PRODUCTS_CODE: code,
            const.BULK_DISCOUNT_UNITS: units,
            const.BULK_DISCOUNT_PRICE: price
        }

        # append in discounts
        discounts.append(dict_bulk_discount)


def group_discount(code, units_ini, units_fin, discounts):
    """This function collects the group discount that is requested for a specific product
    (for example, 2x1 discount on VOUCHER items)
    :param code: product code name
    :param units_ini: chosen units
    :param units_fin: units to pay
    :param discounts: discounts list
    """

    # If the code is existing and the units are positive values
    if len(code) > 0 and units_ini > 0 and units_fin > 0:

        # created the new discount
        dict_group_discount = {
            const.PRODUCTS_CODE: code,
            const.GROUP_DISCOUNT_UNITS_INI: units_ini,
            const.GROUP_DISCOUNT_UNITS_FIN: units_fin
        }

        # append in discounts
        discounts.append(dict_group_discount)


def convert_products(dict_catalog):
    """This function converts our catalog into a list of products
    :param dict_catalog: catalog dictionary containing the configuration for the products
    """

    list_products = []

    # Get values length
    len_row = len(dict_catalog[const.PRODUCTS_CODE])

    # Dictionary created for each product in the article catalog
    for i in range(len_row):
        # new product
        dict_product = {
            const.PRODUCTS_CODE: dict_catalog[const.PRODUCTS_CODE][i],
            const.PRODUCTS_NAME: dict_catalog[const.PRODUCTS_NAME][i],
            const.PRODUCTS_PRICE: dict_catalog[const.PRODUCTS_PRICE][i],
            const.PRODUCTS_UNITS: 0
        }

        # added in final product list
        list_products.append(dict_product)

    return list_products


def catalog_check(dict_catalog):
    """This function verifies that the length of the dictionary values is the same
    :param dict_catalog: catalog dictionary containing the configuration for the products
    """

    len_aux = 0

    # If the json file is empty returns unstable code
    if not dict_catalog:
        logger.error("The json file is empty")
        sys.exit(const.EXIT_CODE_UNSTABLE)

    # Or is not empty see the lengths for values
    else:
        # check values length
        for value in dict_catalog.values():
            len_value = len(value)
            if len_aux == 0:
                len_aux = len_value
            else:
                if len_aux != len_value:
                    logger.info("The json file is not correct by lengths for values")
                    sys.exit(const.EXIT_CODE_BAD)

        # check existing keys at this moment
        if not all(item in list(dict_catalog.keys()) for item in const.PRODUCTS_COLUMNS):
            logger.error("The json file is not correct by columns")
            sys.exit(const.EXIT_CODE_BAD)


def get_products():
    """This function read json configuration with exists products (code, name and price) and created
    dictionaries for this information
    """

    # Path of json configuration
    json_path = const.PATH_JSON_CASH_REGISTER
    logger.info("Reading json file: {}".format(json_path))

    # Get information the exists products
    try:
        json_data = open(json_path)
        dict_catalog = json.load(json_data)
        json_data.close()
    except Exception as ex:
        logger.error("Error load configuration file: {}".format(ex))
        sys.exit(const.EXIT_CODE_BAD)

    # Check catalog information
    catalog_check(dict_catalog)

    # Convert to list from products
    list_products = convert_products(dict_catalog)

    logger.info("Catalog: {}".format(dict_catalog))
    logger.info("Products: {}".format(list_products))

    return dict_catalog, list_products, []


def main():
    catalog, products, discounts = get_products()

    group_discount("VOUCHER", 2, 1, discounts)
    bulk_discount("TSHIRT", 3, 19.00, discounts)

    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("PANTS", products)

    sys.exit(const.EXIT_CODE_OK)


if __name__ == "__main__":
    main()
