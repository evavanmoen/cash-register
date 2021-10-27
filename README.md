# Backend Exercise
**Eva Gutiérrez Vanmoen**


## Explicación:
### /cash-register
El directorio principal consta de varios directorios y del fichero a ejecutar (_cash_register_master.py_).
#### /constants
Dentro el fichero constants.py donde figura todas las constantes a utilizar y el fichero init correspondiente.
#### /input
El fichero _cash_register.json_ consiste en el fichero json de configuración con la información de los \
productos a tratar.
#### /logger
_logger_configurator.py_ utilizado para conseguir el tratamiento de los logs deseado. En este caso \
necesitando ser vistos tanto en local como desde fichero (/logs/cash_register_debug.log).
#### /logs
_cash_register_debug.log_ recoge todos los logs de ejecución.

### cash_register_master.py
Fichero principal y total de todo el proceso. Ejecutable para poder realizar las pruebas propias deseadas \
aunque ya dispone de una función main con distintos casos de prueba pedidos y algunos propios realizados \
pero que se encuentran comentados para dejar que se prueben de uno en uno. \
En el fichero _cash_register_debug.log_ queda recogido todos los mensajes de salida de todas las pruebas realizadas. 

Caso de prueba: 

```tsx
def main():
    catalog, products = get_products()

    logger.info("Catalog: {}".format(catalog))
    logger.info("Products: {}".format(products))

    # EXERCISE CASE 4 (● Items: VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT - Total: 74.50€)
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

    logger.info("Products: {}".format(products))
    logger.info("Total price: {}".format(total(products)))

    sys.exit(const.EXIT_CODE_OK)
```

Y su salida por terminal:
```tsx
/usr/bin/python3.6 /home/eva/PycharmProjects/cash-register/cash_register_master.py
Reading json file: input/cash_register.json
Catalog: {'code': ['VOUCHER', 'TSHIRT', 'PANTS'], 'name': ['Gift Card', 'Summer T-Shirt', 'Summer Pants'], 'price': [5.0, 20.0, 7.5]}
Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 0}]
********************* TEST 4
Scanned a 'VOUCHER' unit
Scanned a 'TSHIRT' unit
Scanned a 'VOUCHER' unit
Scanned a 'VOUCHER' unit
Scanned a 'PANTS' unit
Scanned a 'TSHIRT' unit
Scanned a 'TSHIRT' unit
Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 3}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 3}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 1}]
New group discount on 'VOUCHER' items with 2 units chosen and paid for 1 unit (2x1)
New bulk discount on 'TSHIRT' items with 3 units chosen or more and the price per unit be 19.0
Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 2.0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 19.0, 'units': 3}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 1}]
Total price: 74.5

Process finished with exit code 0
```

#### `main():`
Función main con la ejecución del proceso pedido con varios casos prueba: 
- EXERCISE CASE 1 (● Items: VOUCHER, TSHIRT, PANTS - Total: 32.50€)
- EXERCISE CASE 2 (● Items: VOUCHER, TSHIRT, VOUCHER - Total: 25.00€)
- EXERCISE CASE 3 (● Items: TSHIRT, TSHIRT, TSHIRT, VOUCHER, TSHIRT - Total: 81.00€)
- EXERCISE CASE 4 (● Items: VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT - Total: 74.50€)
- OWN CASE (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, VOUCHER, VOUCHER, VOUCHER, VOUCHER: 84.50€)
- OWN CASE (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 87€)
- OWN CASE (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 79.50€)
- Error discount (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 102€)
- Error discount (VOUCHER, TSHIRT, VOUCHER, VOUCHER, PANTS, TSHIRT, TSHIRT, PANTS, PANTS, PANTS: 79.5€)

#### `catalog_check(dict_catalog):`
Esta función comprueba que la información recogida del json sea correcta y para ello miramos que tratemos con el \
mismo número de valores por clave (es decir, que si recibimos tres código de producto también tengamos tres precios), \
que las claves sean las esperadas (`code`, `name`, `price`) y por último que los precios sean valores positivos. \
Devuelve un mensaje de error o nada si todo se encuentra como debería.

Casos de error (salida recogida en _cash_register_debug.log_):
```tsx
2021-10-27 18:42:11,364 - __main__ - INFO - Reading json file: input/cash_register.json
2021-10-27 18:42:11,364 - __main__ - ERROR - The json file is not correct by negative values
2021-10-27 18:44:01,721 - __main__ - INFO - Reading json file: input/cash_register.json
2021-10-27 18:44:01,721 - __main__ - ERROR - The json file is not correct by columns
```

#### `convert_products(dict_catalog):`
Recibimos el diccionario con el catálogo leído del json de configuración y creamos a partir de dicho diccionario una \
lista de productos, siendo cada producto un diccionario. Y la información sería la misma más la clave `units` añadida \
para llevar el conteo cuando realicemos el escaneo de producto a producto. \
Devuelve la lista de productos del catálogo (`list_products`) o productos a ser añadidos en el carrito (según la \
mención de cada unx).

### `get_products():`
Función encargada de la lectura del json de configuración (_cash_register.json_) para obtener el catálogo de \
productos con los que trataremos. Una vez recogido dicho catálogo en un diccionario (`dict_catalog`) comprobamos con \
la función `catalog_check(dict_catalog)` si recibimos bien la información para cada producto leído. Y por último, \
hacemos uso de la función `convert_products(dict_catalog)` para convertir el json leído a una lista de diccionarios \
conteniendo cada diccionario la información relacionada a un producto. \
Devuelve el diccionario del catálogo (`dict_catalog`) y la lista de productos (`list_products`).

Si todo ha ido bien, este sería un ejemplo de salida tanto del catálogo como de los productos ya separados:
```tsx
2021-10-27 17:49:05,749 - __main__ - INFO - Reading json file: input/cash_register.json
2021-10-27 17:49:05,749 - __main__ - INFO - Catalog: {'code': ['VOUCHER', 'TSHIRT', 'PANTS'], 'name': ['Gift Card', 'Summer T-Shirt', 'Summer Pants'], 'price': [5.0, 20.0, 7.5]}
2021-10-27 17:49:05,749 - __main__ - INFO - Products: [{'code': 'VOUCHER', 'name': 'Gift Card', 'price': 5.0, 'units': 0}, {'code': 'TSHIRT', 'name': 'Summer T-Shirt', 'price': 20.0, 'units': 0}, {'code': 'PANTS', 'name': 'Summer Pants', 'price': 7.5, 'units': 0}]
```

### `scan(code, products):`
Se trata de la función de escaneo de productos recibiendo así el código de producto (`code`) y la lista de productos \
existentes (`products`). Para el producto correspondiente por el código dado se le sumará en uno las unidades de \
producto `p[const.PRODUCTS_UNITS] = p[const.PRODUCTS_UNITS] + 1`. \

### `group_discount(code, units_ini, units_fin, products):`
Descuento para grupo es la función encargada de aplicar los descuentos 2x1, 3x1, 7x1, Nx1... (de momento, ya que a \
futuro podría ser necesario contemplar también ofertas del tipo 3x2 y es por eso que podría añadirse cómodamente \
al código los demás casos, a lo mejor siendo necesario dividir la lógica en funciones más cortas y que esta función \
se quedase englobando el tratamiento de cada caso). \
Por tanto, para lo que se pide en este ejercicio (2x1) realizamos previamente la comprobación de si las unidades del \
producto son mayores o igual a las unidades marcadas en la oferta (`if product[const.PRODUCTS_UNITS] >= units_ini:`) \
para saber si es aplicable en el producto y si sí se da dicha comprobación pasaríamos entonces a preguntarnos si \
si se trata de una oferta Nx1 (`if units_fin == 1:`). Una vez sepamos que sí podemos aplicar esta oferta faltaría \
tratar por separado si las unidades del producto es un número par o impar ya que la resolución de cuántos productos \
pagaríamos al finalizar la compra sería diferente. \
Si se trata de un número par las unidades finales a pagar pasarían a ser las actuales divididas entre las unidades \
ofertadas: 
```tsx
if product[const.PRODUCTS_UNITS] % units_ini == 0:
    product[const.PRODUCTS_UNITS] = product[const.PRODUCTS_UNITS] / units_ini
 ``` 
Y si se trata de un número impar el cálculo se realizaría restando 1 a las unidades actuales, dividir entre las \
unidades ofertadas y esa unidad restada de antes sumarla al resultado de la división:
```tsx
elif product[const.PRODUCTS_UNITS] % units_ini != 0:
    units = product[const.PRODUCTS_UNITS]
    units -= 1
    product[const.PRODUCTS_UNITS] = (units / units_ini) + 1
```
Si no existe un producto con el código dado enviamos al log y mostramos por pantalla un mensaje de aviso:
```tsx
2021-10-27 17:04:52,147 - __main__ - INFO - Not exist 'SHOES' product in cart
```

### `bulk_discount(code, units, price, products):`
Descuento a granel recibe un mínimo de unidades existentes y el cambio a un precio nuevo (en el caso ejemplo del \
ejercicio se nos pide que por 3 o más VOUCHER unidades el precio por unidad pasa a ser de 19.00). Por tanto si \
existe el producto que se corresponde al código dado miramos si sus unidades son igual o mayor al mínimo dado y en \
caso afirmativo el valor de la clave precio pasa a valer lo que el nuevo precio marque:
```tsx
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
```

### `total(products):`
Y por último, esta función se encarga de calcular el precio total a pagar por todo el carrito. Es decir, \
recorremos cada producto y obtenemos su total multiplicando las unidades leídas de dicho producto por su precio \
unidad y sumando el resultado con el mismo cálculo para el siguiente producto. \
Por tanto, devuelve el precio total a pagar (`total_price`).