from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Productos, Facturas, Albaran, albaran_producto, factura_producto
from forms import AlbaranForm, FacturaForm
from sqlalchemy import update

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "MySecretKey"

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()


create_tables()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stock')
def stock():
    productos = Productos.query.all()
    return render_template('productos.html', productos=productos)

from flask import request, redirect, url_for

@app.route('/editar_precio/<int:producto_id>', methods=['POST'])
def editar_precio(producto_id):
    if request.method == 'POST':
        # Obtiene el nuevo precio del formulario enviado
        nuevo_precio = request.form['precio']
        # Busca el producto por su ID en la base de datos
        producto = Productos.query.get(producto_id)
        # Verifica si se encontró el producto
        if producto:
            # Actualiza el precio del producto con el nuevo precio
            producto.precio = nuevo_precio
            # Guarda los cambios en la base de datos
            db.session.commit()
            # Redirige a la página de stock después de editar el precio
            return redirect(url_for('stock'))
        else:
            return redirect(url_for('stock'))
    else:
        return redirect(url_for('stock'))

@app.route('/cambiar_estado_producto/<int:producto_id>', methods=['POST'])
def cambiar_estado_producto(producto_id):
    producto = Productos.query.get_or_404(producto_id)
    
    # Obtener el nuevo estado del producto del formulario
    nuevo_estado = request.form.get('habilitado', None)
    if nuevo_estado is None:
        
        return redirect(url_for('productos'))

    # Convertir el nuevo estado a un valor booleano
    nuevo_estado = nuevo_estado.lower() == 'true'

    # Actualizar el estado del producto
    producto.habilitado = nuevo_estado
    db.session.commit()

    # Redirigir de vuelta a la página de productos
    return redirect(url_for('stock'))

@app.route('/facturas', methods=["GET", "POST"])
def facturas():
    # Crea una instancia del formulario de Factura
    form = FacturaForm()
    # Obtiene todos los productos habilitados de la base de datos
    productos_habilitados = Productos.query.filter_by(habilitado=True).all()  # Filtrar solo productos habilitados
    
    if request.method == 'POST' and form.validate_on_submit():
        # Crea una nueva factura con la fecha actual y un total inicial de 0
        factura = Facturas(fecha=datetime.utcnow(), total=0)
        db.session.add(factura)
        db.session.commit()
        
        for i in range(1, 5):
            nombre_field = getattr(form, f'nom{i}')
            cantidad_field = getattr(form, f'cantidad{i}')
            nombre = nombre_field.data
            cantidad = cantidad_field.data
            
            # Verifica si se proporcionó un nombre de producto y una cantidad
            if nombre and cantidad:
                # Busca el producto en la base de datos por su nombre y verifica si está habilitado
                producto = Productos.query.filter_by(nombre=nombre, habilitado=True).first()
                
                if producto:
                    # Verifica si hay suficiente cantidad en stock del producto seleccionado
                    if producto.cantidad >= cantidad:
                        total_producto = cantidad * producto.precio
                        
                        # Añadimos los datos a factura_producto
                        factura_producto_insert = factura_producto.insert().values(
                            factura_id=factura.id,
                            producto_id=producto.id,
                            cantidad=cantidad,
                            total=total_producto
                        )

                        db.session.execute(factura_producto_insert)
                        factura.total += total_producto  # Sumar al total de la factura
                        producto.cantidad -= cantidad # Reduce la cantidad en stock del producto
                    else:
                        print(f"No hay suficiente cantidad de {producto.nombre} en stock.")
                else:
                    print(f"No se encontró el producto con nombre '{nombre}' en la base de datos o no está habilitado.")
        
        db.session.commit()
        print("Factura procesada correctamente")
        return redirect(url_for("stock"))
    
    # Renderiza la plantilla de facturas con los productos habilitados y el formulario
    return render_template("facturas.html", productos=productos_habilitados, form=form)


@app.route('/albaranes', methods=['GET', 'POST'])
def albaranes():
    # Crea una instancia del formulario de Albarán
    form = AlbaranForm()

    if request.method == 'POST' and form.validate():
        # Crea un nuevo albarán con la fecha actual
        albaran = Albaran()
        albaran.fecha = datetime.utcnow()
        db.session.add(albaran)
        db.session.commit()

        for i in range(1, 5):
            nombre_field = getattr(form, f'nom{i}')
            cantidad_field = getattr(form, f'cantidad{i}')
            nombre = nombre_field.data
            cantidad = cantidad_field.data

            # Verifica si se proporcionó un nombre de producto y una cantidad
            if nombre and cantidad:
                # Busca si el producto ya existe en la base de datos
                product_exists = Productos.query.filter_by(nombre=nombre).first()

                if product_exists:
                    # Si el producto existe, actualiza su cantidad en stock y asocia el producto al albarán
                    product_exists.cantidad += cantidad
                    albaran.productos.append(product_exists)
                    db.session.commit()
                    # Actualiza la cantidad del producto en el albarán_producto
                    db.session.execute(update(albaran_producto).where(albaran_producto.c.producto_id == product_exists.id).values(cantidad=cantidad))
                    db.session.commit()
                else:
                    # Si el producto no existe, crea uno nuevo y lo añade al albarán
                    new_product = Productos(nombre=nombre, cantidad=cantidad)
                    albaran.productos.append(new_product)
                    db.session.add(new_product)
                    db.session.commit()
                    # Actualiza la cantidad del producto en el albarán_producto
                    db.session.execute(update(albaran_producto).where(albaran_producto.c.producto_id == new_product.id).values(cantidad=cantidad))
                    db.session.commit()

    # Renderiza la plantilla de albaranes con el formulario
    return render_template('albaran.html', form=form)