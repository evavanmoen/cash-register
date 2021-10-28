#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

import constants.constants as const
import logger.logger_configurator as logger_configurator

logger = logger_configurator.get_logger(__name__)


def total(products):
    """This function calculates the total price of the products cart
    :param products: products cart
    """

    total_price = 0

    for product in products:
        total_price += product[const.PRODUCTS_UNITS] * product[const.PRODUCTS_PRICE]

    return total_price


def scan(code, products):
    """This function gets code to scan and add 1 unit in field units in the correspondent dictionary
    :param code: product code name
    :param products: list with exists products
    """

    exist = False

    # Add a unit to the product corresponding to the given code
    for p in products:
        if p[const.PRODUCTS_CODE] == code:
            p[const.PRODUCTS_UNITS] = p[const.PRODUCTS_UNITS] + 1
            exist = True
            logger.info("Scanned a '{}' unit".format(code))

    # Not exist this product in our catalog
    if not exist:
        logger.error("Error scanning a '{}' unit because the product is not registered in the catalog".format(code))


def bulk_discount(code, units, price, products):
    """This function collects the bulk discount that is requested for a specific product
    (for example, 3 or more TSHIRT items, the price per unit should be 19.00€)
    :param code: product code name
    :param units: units mark at discount
    :param price: new item price
    :param products: list with exists products in cart
    """

    # If the code is existing and the unit and price are positive values
    if len(code) > 0 and units > 0 and price > 0.0 and type(units) == int:

        exist = False

        # Change price in the correcting product only the condition is true
        for product in products:
            if product[const.PRODUCTS_CODE] == code:

                exist = True

                if product[const.PRODUCTS_UNITS] >= units:
                    product[const.PRODUCTS_PRICE] = price
                    logger.info(
                        "New bulk discount on '{}' items with {} units chosen or more and the price per unit be {}".
                        format(code, units, price))
                else:
                    break

        if not exist:
            logger.info("Bulk discount not applied: not exist '{}' product in cart".format(code, units, price))

    else:
        logger.info("Bulk discount not applied: invalid parameters")


def group_discount(code, units_ini, units_fin, products):
    """This function collects the group discount that is requested for a specific product
    (for example, 2x1 discount on VOUCHER items and at the moment any number of items x 1)
    :param code: product code name
    :param units_ini: chosen units
    :param units_fin: units to pay
    :param products: list with exists products in cart
    """

    # If the code is existing and the units are positive values
    if len(code) > 0 and units_ini > 0 and units_fin > 0 and type(units_ini) == int:

        exist = False

        # Check that the product to make this discount exists
        for product in products:
            if product[const.PRODUCTS_CODE] == code:

                exist = True

                # if have the minimum number of products to apply the discount
                if product[const.PRODUCTS_UNITS] >= units_ini:

                    # discounts 2x1, 3x1, (allx1) ...
                    if units_fin == 1:

                        # if the number units is even
                        if product[const.PRODUCTS_UNITS] % units_ini == 0:
                            product[const.PRODUCTS_UNITS] = product[const.PRODUCTS_UNITS] / units_ini

                        # or the number units is odd
                        elif product[const.PRODUCTS_UNITS] % units_ini != 0:
                            units = product[const.PRODUCTS_UNITS]
                            units -= 1
                            product[const.PRODUCTS_UNITS] = (units / units_ini) + 1

                        logger.info("New group discount on '{0}' items with {1} units chosen and paid for {2} unit "
                                    "({1}x{2})".format(code, units_ini, units_fin))
                else:
                    break

        if not exist:
            logger.info("Group discount not applied: not exist '{}' product in cart".format(code, units_ini, units_fin))

    else:
        logger.info("Group discount not applied: invalid parameters")


def convert_products(dict_catalog):
    """This function converts our catalog into a list of products
    :param dict_catalog: catalog dictionary containing the configuration for the products
    """

    list_products = []

    # Get values length
    len_row = len(dict_catalog[const.PRODUCTS_CODE])

    # Dictionary created for each product in the article catalog
    for i in range(len_row):

        # created new product
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

    # Or if is not empty check the lengths, price value and if it is the correct columns
    else:

        # check values length
        for key, value in dict_catalog.items():

            # if exists negative prices returns error
            if key == const.PRODUCTS_PRICE:
                for v in value:
                    if v < 0:
                        logger.error("The json file is not correct by negative values")
                        sys.exit(const.EXIT_CODE_BAD)

            # if exists values with different size returns error
            len_value = len(value)
            if len_aux == 0:
                len_aux = len_value
            else:
                if len_aux != len_value:
                    logger.error("The json file is not correct by lengths for values")
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

    return dict_catalog, list_products


def main():
    catalog, products = get_products()

    logger.info("Catalog: {}".format(catalog))
    logger.info("Products: {}".format(products))

    # CASE 1 (Items: VOUCHER, TSHIRT, PANTS - Total: 32.50€)
    # (with 2x1 in VOUCHER items and 3 or more TSHIRT items the price per unit should be 19.00)
    """
    logger.info("********************* TEST 1")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("PANTS", products)
    
    logger.info("Products: {}".format(products))
    group_discount("VOUCHER", 2, 1, products)
    bulk_discount("TSHIRT", 3, 19.00, products)"""

    # CASE 2 (Items: VOUCHER, TSHIRT, VOUCHER - Total: 25.00€)
    # (with 2x1 in VOUCHER items and 3 or more TSHIRT items the price per unit should be 19.00)
    """
    logger.info("********************* TEST 2")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    
    logger.info("Products: {}".format(products))
    group_discount("VOUCHER", 2, 1, products)
    bulk_discount("TSHIRT", 3, 19.00, products)"""

    # CASE 3 (Items: TSHIRT, TSHIRT, TSHIRT, VOUCHER, TSHIRT - Total: 81.00€)
    # (with 2x1 in VOUCHER items and 3 or more TSHIRT items the price per unit should be 19.00)
    """
    logger.info("********************* TEST 3")
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    
    logger.info("Products: {}".format(products))
    group_discount("VOUCHER", 2, 1, products)
    bulk_discount("TSHIRT", 3, 19.00, products)"""

    # CASE 4 (Items: VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT - Total: 74.50€)
    # (with 2x1 in VOUCHER items and 3 or more TSHIRT items the price per unit should be 19.00)
    logger.info("********************* TEST 4")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("PANTS", products)
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    
    logger.info("Products: {}".format(products))
    group_discount("VOUCHER", 2, 1, products)
    bulk_discount("TSHIRT", 3, 19.00, products)

    # CASE 5 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, VOUCHER, VOUCHER, VOUCHER, VOUCHER: 84.50€)
    # (with 2x1 in VOUCHER items and 3 or more TSHIRT items the price per unit should be 19.00)
    """
    logger.info("********************* TEST 5 (own test for 2x1 in VOUCHER items but got more VOUCHER items)")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("PANTS", products)
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    
    logger.info("Products: {}".format(products))
    group_discount("VOUCHER", 2, 1, products)
    bulk_discount("TSHIRT", 3, 19.00, products)"""

    # CASE 6 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 87€)
    # (with 3x1 in PANTS items and 3 or more TSHIRT items the price per unit should be 19.00)
    """
    logger.info("********************* TEST 6 (own test for 3x1 in PANTS items)")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("PANTS", products)
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    scan("PANTS", products)
    scan("PANTS", products)
    scan("PANTS", products)

    logger.info("Products: {}".format(products))
    group_discount("PANTS", 3, 1, products)
    bulk_discount("TSHIRT", 3, 19.00, products)"""

    # CASE 7 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 79.50€)
    # (with 4x1 in PANTS items and 3 or more TSHIRT items the price per unit should be 19.00)
    """
    logger.info("********************* TEST 7 (own test for 4x1 in PANTS items)")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("PANTS", products)
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    scan("PANTS", products)
    scan("PANTS", products)
    scan("PANTS", products)
    
    logger.info("Products: {}".format(products))
    group_discount("PANTS", 4, 1, products)
    bulk_discount("TSHIRT", 3, 19.00, products)"""

    # CASE 8 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 102€)
    # (with 2x1 in SHOES items and 2 or more VOUCHER items the price per unit should be 4.00)
    """
    logger.info("********************* TEST 8 (error case with 2x1 in SHOES items because not got SHOES items)")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("PANTS", products)
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    scan("PANTS", products)
    scan("PANTS", products)
    scan("PANTS", products)

    logger.info("Products: {}".format(products))
    group_discount("SHOES", 2, 1, products)
    bulk_discount("VOUCHER", 2, 4.00, products)"""

    # CASE 9 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 79.5€)
    # (with 2x1 in SHOES items and 2 or more VOUCHER items the price per unit should be 4.00 and 4x1 in PANTS items)
    """
    logger.info("********************* TEST 9 (error case with 2x1 in SHOES items because not got SHOES items)")
    scan("VOUCHER", products)
    scan("TSHIRT", products)
    scan("VOUCHER", products)
    scan("VOUCHER", products)
    scan("PANTS", products)
    scan("TSHIRT", products)
    scan("TSHIRT", products)
    scan("PANTS", products)
    scan("PANTS", products)
    scan("PANTS", products)

    logger.info("Products: {}".format(products))
    group_discount("SHOES", 2, 1, products)
    bulk_discount("VOUCHER", 2, 4.00, products)
    group_discount("PANTS", 4, 1, products)"""

    logger.info("Products: {}".format(products))
    logger.info("Total price: {}".format(total(products)))

    sys.exit(const.EXIT_CODE_OK)


if __name__ == "__main__":
    main()
