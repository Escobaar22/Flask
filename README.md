1º La aplicación se inicia con el comando 'python -m flask --app app.py run'.

2º Al iniciarla se creará el archivo data.sqlite donde se podrán ver las tablas creadas y los datos que se vayan añadiendo a estas.

3º Entraremos a la siguiente ruta para ver la parte visual de la aplicación después de arrancarla con el comando del paso 1: http://127.0.0.1:5000/.

4º Lo primero que debemos hacer es acceder a la pestaña Albaranes. Añadiremos el nombre del producto que deseemos y la cantidad.

5º Para comprobar si el producto se ha añadido, iremos a la pestaña Productos donde aparecerán los productos de la tabla Productos.

6º En esta pestaña mismo podremos habilitar o deshabilitar los productos, además de que debemos añadirles un precio para poder crear las facturas a posteriori. El precio de los productos lo pondrá el usuario a su placer; el formato del precio es 0,00, ya que el tipo de dato en la base de datos es un float.

7º Una vez tengamos productos añadidos (y habilitados), podremos hacer un pedido en la pestaña Facturas. Una vez ahí, tendremos un desplegable donde veremos los productos habilitados e introduciremos la cantidad que queramos pedir. En caso de introducir un valor mayor al disponible, no se disminuirá la cantidad del producto seleccionado.

Extras:

-- Si el producto está deshabilitado, no se mostrará en el desplegable de la pestaña Facturas.

-- Si en la pestaña Albaranes introducimos el nombre de un producto que ya existe en la base de datos, se sumará la cantidad especificada a la que ya tengamos.