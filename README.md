# Backend Exercise
**Eva Gutiérrez Vanmoen**

## Enunciado:
X is thinking about expanding its business and not only forecast sales in the stores but
also manage the cash register. The first store where we will introduce our software will sell the
following 3 products.
CODE NAME PRICE
VOUCHER Gift Card 5.00€
TSHIRT Summer T-Shirt 20.00€
PANTS Summer Pants 7.50€
The different departments have agreed the following discounts:
- A 2-for-1 special on VOUCHER items.
- If you buy 3 or more TSHIRT items, the price per unit should be 19.00€.
- Items can be scanned in any order, and the cashier should return the total amount to be
paid.

The interface for the checkout process has the following specifications:
- The Checkout constructor receives a pricing_rules object
- The Checkout object has a scan method that receives one item at a time

Examples:
- Items: VOUCHER, TSHIRT, PANTS - Total: 32.50€
- Items: VOUCHER, TSHIRT, VOUCHER - Total: 25.00€
- Items: TSHIRT, TSHIRT, TSHIRT, VOUCHER, TSHIRT - Total: 81.00€
- Items: VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT - Total: 74.50€

## Explicación:
### /cash-register
El directorio principal consta de varios directorios y del fichero a ejecutar (_cash_register_master.py_).
- #### /constants
  Incluye el fichero _constants.py_ donde figuran todas las constantes a utilizar y el fichero init correspondiente.
- #### /input
  Incluye _cash_register.json_, que consiste en el fichero .json con la información de los productos a tratar.
- #### /logger
  Incluye _logger_configurator.py_, utilizado para conseguir el tratamiento de los logs deseado. En este caso \
necesitando ser vistos tanto en local como desde fichero (/logs/_cash_register_debug.log_).
- #### /logs
  Incluye _cash_register_debug.log_, el cual recoge los logs de ejecución de todas las pruebas realizadas.

### _cash_register_master.py_
Fichero principal que contiene toda la lógica del proceso, que incluye las funciones necesarias para cumplir con \
las especificaciones de este ejercicio. 
- Función de lectura de configuración de .json `get_products()`
- Función de escaneo de productos uno-a-uno `scan(code, products)`
- Función de aplicación de promoción grupal `group_discount(code, units_ini, units_fin, products)`
- Función de aplicación de promoción al por mayor `bulk_discount(code, units, price, products)`
- Función de cálculo del coste total `total(products)`
- Funciones auxiliares `catalog_check(dict_catalog)` y `convert_products(dict_catalog)`
- Función `main()` con los casos de prueba requeridos y algunos otros adicionales que dejo comentados para \
que puedan probarse de uno en uno. 

 #### Caso de prueba 
  
  ```tsx
  def main():
      catalog, products = get_products()
  
      logger.info("Catalog: {}".format(catalog))
      logger.info("Products: {}".format(products))
  
      # ...
  
      # CASE 3 (Items: TSHIRT, TSHIRT, TSHIRT, VOUCHER, TSHIRT - Total: 81.00€)
      # (with 2x1 in VOUCHER items and 3 or more TSHIRT items the price per unit should be 19.00)
      logger.info("********************* TEST 3")
      scan("TSHIRT", products)
      scan("TSHIRT", products)
      scan("TSHIRT", products)
      scan("VOUCHER", products)
      scan("TSHIRT", products)
      
      logger.info("Products: {}".format(products))
      group_discount("VOUCHER", 2, 1, products)
      bulk_discount("TSHIRT", 3, 19.00, products)
  
      # ...
  
      logger.info("Products: {}".format(products))
      logger.info("Total price: {}".format(total(products)))
  
      sys.exit(const.EXIT_CODE_OK)
  ```

  Salida por la terminal de PyCharm:
  ```tsx
  /usr/bin/python3.6 /home/eva/Escritorio/PRUEBAS-TECNICAS/Nextail/cash-register/cash_register_master.py
  Reading json file: input/cash_register.json
  Catalog: {'code': ['VOUCHER', 'TSHIRT', 'PANTS'], 'name': ['Gift Card', 'Summer T-Shirt', 'Summer Pants'], 'price': [5.0, 20.0, 7.5]}
  Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 0, 'total_price': 0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 0, 'total_price': 0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 0, 'total_price': 0}]
  ********************* TEST 3
  Scanned a 'TSHIRT' unit
  Scanned a 'TSHIRT' unit
  Scanned a 'TSHIRT' unit
  Scanned a 'VOUCHER' unit
  Scanned a 'TSHIRT' unit
  Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 1, 'total_price': 5.0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 4, 'total_price': 80.0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 0, 'total_price': 0}]
  New bulk discount on 'TSHIRT' items with 3 units chosen or more and the price per unit be 19.0
  Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 1, 'total_price': 5.0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 19.0, 'units': 4, 'total_price': 76.0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 0, 'total_price': 0}]
  Total cart price: 81.0
  
  Process finished with exit code 0
  ```


### Funciones de _cash_register_master.py_

A continuación se muestran los detalles de la lógica de cada función:

- ### `main():` 

  Función prueba con los casos requeridos por la prueba: 
  - CASE 1 (Items: VOUCHER, TSHIRT, PANTS - Total: 32.50€)
  - CASE 2 (Items: VOUCHER, TSHIRT, VOUCHER - Total: 25.00€)
  - CASE 3 (Items: TSHIRT, TSHIRT, TSHIRT, VOUCHER, TSHIRT - Total: 81.00€)
  - CASE 4 (Items: VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT - Total: 74.50€)
  
  Y algunos casos adicionales:
  - CASE 5 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, VOUCHER, VOUCHER, VOUCHER, VOUCHER: 84.50€)
  - CASE 6 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 87€)
  - CASE 7 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 79.50€)
  - CASE 8 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 102€)
  - CASE 9 (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 79.5€)
  

- ### `get_products():`
  Función encargada de la lectura del .json (_cash_register.json_) para obtener el catálogo de productos con los \
que trataremos. Una vez recogido dicho catálogo en un diccionario (`dict_catalog`), comprobamos con la \
función `catalog_check(dict_catalog)` si la información es válida. Por último, hacemos uso de la función \
`convert_products(dict_catalog)` para convertir `dict_catalog` en una lista de diccionarios. Cada uno de \
esos diccionarios contiene la información de un producto. \
Esta función nos devuelve el diccionario del catálogo (`dict_catalog`) y la lista de productos \
(`list_products`). \
A continuación se muestra lo que sería un print en la salida de _cash_register_debug.log_:

  ```tsx
  2021-10-27 17:49:05,749 - __main__ - INFO - Reading json file: input/cash_register.json
  2021-10-27 17:49:05,749 - __main__ - INFO - Catalog: {'code': ['VOUCHER', 'TSHIRT', 'PANTS'], 'name': ['Gift Card', 'Summer T-Shirt', 'Summer Pants'], 'price': [5.0, 20.0, 7.5]}
  2021-10-27 17:49:05,749 - __main__ - INFO - Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 0}]
  ```

  - #### `catalog_check(dict_catalog):`
    Esta función comprueba que la información recogida del .json sea válida. Comprobamos que exista el \
mismo número de valores en cada clave (`code`, `name` y `price`), y que los precios sean valores \
positivos. \
La función devuelve un mensaje de error si la información no es válida.
    ```tsx
    2021-10-27 18:42:11,364 - __main__ - INFO - Reading json file: input/cash_register.json
    2021-10-27 18:42:11,364 - __main__ - ERROR - The json file is not correct by negative values
    2021-10-27 18:44:01,721 - __main__ - INFO - Reading json file: input/cash_register.json
    2021-10-27 18:44:01,721 - __main__ - ERROR - The json file is not correct by columns
    ```

  - #### `convert_products(dict_catalog):`
    Esta función convierte el diccionario `dict_catalog`  en una lista de productos, añadiendo las \
claves `total_price` y `units` con valores iniciales a 0. `units` sirve para llevar el conteo cuando \
realicemos el escaneo producto a producto. \
Devuelve la lista de productos del catálogo (`list_products`).

- ### `scan(code, products):`
  Se trata de la función de escaneo de productos del carrito de compra, recibiendo así el código de producto \
(`code`) y la lista de productos existentes (`products`). Al producto correspondiente a este `code` se le \
sumará en uno las unidades de producto y calcularemos su precio total multiplicando sus unidades por su \
precio unidad.

- ### `group_discount(code, units_ini, units_fin, products):`
  Función encargada de aplicar los descuentos nx1, siendo n cualquier número entero positivo (`units_ini`). \
En el caso contemplado en este ejercicio, una vez encontrado el producto que se corresponde con el código \
(`code`), realizamos primero la comprobación de si el tipo de producto es elegible  para aplicar esta oferta, \
evaluando su número de escaneos (`if product[const.PRODUCTS_UNITS] >= units_ini:`) en relación a 'n'. \
Si el producto es elegible, comprobamos si se trata de una oferta nx1 (`if units_fin == 1:`). \
Una vez sepamos que podemos aplicar esta oferta, miramos si las unidades del producto escaneadas son \
divisibles entre 'n'.

  - Si se trata de un número divisible, las unidades a pagar son las unidades escaneadas divididas entre 'n', \
el factor de oferta: 
  ```tsx
  if product[const.PRODUCTS_UNITS] % units_ini == 0:
      product[const.PRODUCTS_UNITS] = product[const.PRODUCTS_UNITS] / units_ini
   ``` 
  - Si se trata de un número no divisible, el cálculo de unidades a pagar se realiza aplicando la operación \
anterior al número par inferior (restando una unidad) y sumándole al resultado la unidad restante.
  ```tsx
  elif product[const.PRODUCTS_UNITS] % units_ini != 0:
      units = product[const.PRODUCTS_UNITS]
      units -= 1
      product[const.PRODUCTS_UNITS] = (units / units_ini) + 1
  ```
  Y por último lugar, quedaría recalcular el precio total de dicho producto:
  ```tsx
  product[const.PRODUCTS_TOTAL_PRICE] = product[const.PRODUCTS_UNITS] * product[const.PRODUCTS_PRICE]
  ```
  Si no existe un producto con el código dado, enviamos al log y por pantalla un mensaje de aviso:
  ```tsx
  2021-10-27 17:04:52,147 - __main__ - INFO - Not exist 'SHOES' product in cart
  ```

- ### `bulk_discount(code, units, price, products):`
  La función de descuento por compra al por mayor recibe el código del producto, el número mínimo de \
unidades a partir del cual se aplica la oferta, el precio del artículo en promoción y la lista de los \
productos en el carrito de compra. Si existe el producto que se corresponde al código dado, se comprueba \
si el tipo de producto es elegible para aplicar esta oferta, teniendo en cuenta su número de escaneos y \
la configuración de la oferta. \
Si el producto es elegible para la oferta, el precio del producto pasa a ser el precio definido en la oferta y \
terminríamos con el recálculo del precio total:
  ```tsx
  for product in products:
      if product[const.PRODUCTS_CODE] == code:

          exist = True

          if product[const.PRODUCTS_UNITS] >= units:
              product[const.PRODUCTS_PRICE] = price
              product[const.PRODUCTS_TOTAL_PRICE] = product[const.PRODUCTS_UNITS] * product[const.PRODUCTS_PRICE]
              logger.info(
                  "New bulk discount on '{}' items with {} units chosen or more and the price per unit be {}".
                  format(code, units, price))
          else:
              break
  ```

- ### `total(products):`
  Finalmente, esta función se encarga de calcular el precio final a pagar por todo el carrito de compra. \
Es decir, sumando los precios totales (`total_price`) de los productos. Esta función devuelve el precio \
final a pagar (`final_price`).

## Ejecución:
El proceso se puede ejecutar desde terminal o desde cualquier plataforma mediante el fichero _cash_register_master.py_. 

- Ejecución desde terminal:
  ```tsx
  eva@eva-Modern-14-B10MW:~/PycharmProjects/cash-register$ python cash_register_master.py 
  2021-10-28 10:00:22,125 - __main__ - INFO - Reading json file: input/cash_register.json
  Reading json file: input/cash_register.json
  2021-10-28 10:00:22,126 - __main__ - INFO - Catalog: {u'price': [5.0, 20.0, 7.5], u'code': [u'VOUCHER', u'TSHIRT', u'PANTS'], u'name': [u'Gift Card', u'Summer T-Shirt', u'Summer Pants']}
  Catalog: {u'price': [5.0, 20.0, 7.5], u'code': [u'VOUCHER', u'TSHIRT', u'PANTS'], u'name': [u'Gift Card', u'Summer T-Shirt', u'Summer Pants']}
  2021-10-28 10:00:22,126 - __main__ - INFO - Products: [{'units': 0, 'total_price': 0, 'price': 5.0, 'code': u'VOUCHER', 'name': u'Gift Card'}, {'units': 0, 'total_price': 0, 'price': 20.0, 'code': u'TSHIRT', 'name': u'Summer T-Shirt'}, {'units': 0, 'total_price': 0, 'price': 7.5, 'code': u'PANTS', 'name': u'Summer Pants'}]
  Products: [{'units': 0, 'total_price': 0, 'price': 5.0, 'code': u'VOUCHER', 'name': u'Gift Card'}, {'units': 0, 'total_price': 0, 'price': 20.0, 'code': u'TSHIRT', 'name': u'Summer T-Shirt'}, {'units': 0, 'total_price': 0, 'price': 7.5, 'code': u'PANTS', 'name': u'Summer Pants'}]
  2021-10-28 10:00:22,126 - __main__ - INFO - ********************* TEST 4
  ********************* TEST 4
  2021-10-28 10:00:22,126 - __main__ - INFO - Scanned a 'VOUCHER' unit
  Scanned a 'VOUCHER' unit
  2021-10-28 10:00:22,126 - __main__ - INFO - Scanned a 'TSHIRT' unit
  Scanned a 'TSHIRT' unit
  2021-10-28 10:00:22,126 - __main__ - INFO - Scanned a 'VOUCHER' unit
  Scanned a 'VOUCHER' unit
  2021-10-28 10:00:22,126 - __main__ - INFO - Scanned a 'VOUCHER' unit
  Scanned a 'VOUCHER' unit
  2021-10-28 10:00:22,126 - __main__ - INFO - Scanned a 'PANTS' unit
  Scanned a 'PANTS' unit
  2021-10-28 10:00:22,126 - __main__ - INFO - Scanned a 'TSHIRT' unit
  Scanned a 'TSHIRT' unit
  2021-10-28 10:00:22,126 - __main__ - INFO - Scanned a 'TSHIRT' unit
  Scanned a 'TSHIRT' unit
  2021-10-28 10:00:22,126 - __main__ - INFO - Products: [{'units': 3, 'total_price': 15.0, 'price': 5.0, 'code': u'VOUCHER', 'name': u'Gift Card'}, {'units': 3, 'total_price': 60.0, 'price': 20.0, 'code': u'TSHIRT', 'name': u'Summer T-Shirt'}, {'units': 1, 'total_price': 7.5, 'price': 7.5, 'code': u'PANTS', 'name': u'Summer Pants'}]
  Products: [{'units': 3, 'total_price': 15.0, 'price': 5.0, 'code': u'VOUCHER', 'name': u'Gift Card'}, {'units': 3, 'total_price': 60.0, 'price': 20.0, 'code': u'TSHIRT', 'name': u'Summer T-Shirt'}, {'units': 1, 'total_price': 7.5, 'price': 7.5, 'code': u'PANTS', 'name': u'Summer Pants'}]
  2021-10-28 10:00:22,126 - __main__ - INFO - New group discount on 'VOUCHER' items with 2 units chosen and paid for 1 unit (2x1)
  New group discount on 'VOUCHER' items with 2 units chosen and paid for 1 unit (2x1)
  2021-10-28 10:00:22,126 - __main__ - INFO - New bulk discount on 'TSHIRT' items with 3 units chosen or more and the price per unit be 19.0
  New bulk discount on 'TSHIRT' items with 3 units chosen or more and the price per unit be 19.0
  2021-10-28 10:00:22,126 - __main__ - INFO - Products: [{'units': 2, 'total_price': 10.0, 'price': 5.0, 'code': u'VOUCHER', 'name': u'Gift Card'}, {'units': 3, 'total_price': 57.0, 'price': 19.0, 'code': u'TSHIRT', 'name': u'Summer T-Shirt'}, {'units': 1, 'total_price': 7.5, 'price': 7.5, 'code': u'PANTS', 'name': u'Summer Pants'}]
  Products: [{'units': 2, 'total_price': 10.0, 'price': 5.0, 'code': u'VOUCHER', 'name': u'Gift Card'}, {'units': 3, 'total_price': 57.0, 'price': 19.0, 'code': u'TSHIRT', 'name': u'Summer T-Shirt'}, {'units': 1, 'total_price': 7.5, 'price': 7.5, 'code': u'PANTS', 'name': u'Summer Pants'}]
  2021-10-28 10:00:22,126 - __main__ - INFO - Total cart price: 74.5
  Total cart price: 74.5

  ```

- Ejecución desde PyCharm:
  ```tsx
  /usr/bin/python3.6 /home/eva/PycharmProjects/cash-register/cash_register_master.py
  Reading json file: input/cash_register.json
  Catalog: {'code': ['VOUCHER', 'TSHIRT', 'PANTS'], 'name': ['Gift Card', 'Summer T-Shirt', 'Summer Pants'], 'price': [5.0, 20.0, 7.5]}
  Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 0, 'total_price': 0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 0, 'total_price': 0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 0, 'total_price': 0}]
  ********************* TEST 4
  Scanned a 'VOUCHER' unit
  Scanned a 'TSHIRT' unit
  Scanned a 'VOUCHER' unit
  Scanned a 'VOUCHER' unit
  Scanned a 'PANTS' unit
  Scanned a 'TSHIRT' unit
  Scanned a 'TSHIRT' unit
  Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 3, 'total_price': 15.0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 3, 'total_price': 60.0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 1, 'total_price': 7.5}]
  New group discount on 'VOUCHER' items with 2 units chosen and paid for 1 unit (2x1)
  New bulk discount on 'TSHIRT' items with 3 units chosen or more and the price per unit be 19.0
  Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 2.0, 'total_price': 10.0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 19.0, 'units': 3, 'total_price': 57.0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 1, 'total_price': 7.5}]
  Total cart price: 74.5

  Process finished with exit code 0
  ```

## Comentarios adicionales:
#### Descuentos 2x1:
El código está hecho de tal forma que no solo contemplamos la oferta requerida sino que se trataría con ofertas \
de todo número x 1 ya que siguen el mismo cálculo de reajuste de unidades a pagar una vez aplicado el descuento.

#### Función `total()`:
Esta función tuvo una primera versión donde se realizada el cálculo final del carrito haciendo el cálculo total \
de cada producto mirando su número de unidades y precio unidad. En la versión actual realiza solo la suma de \
los totales ya que cada precio total de producto se encuentra ya calculado y guardado en el campo \
`total_price` de cada producto.

\
![Alt text](uno.png?raw=true)