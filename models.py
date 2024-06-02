from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

factura_producto = Table('factura_producto', db.Model.metadata,
    db.Column('factura_id', db.Integer, ForeignKey('facturas.id')),
    db.Column('producto_id', db.Integer, ForeignKey('productos.id')),
    db.Column('cantidad', db.Integer),
    db.Column('total', db.Float)
)

albaran_producto = Table('albaran_producto', db.Model.metadata,
    db.Column('albaran_id', db.Integer, ForeignKey('albaran.id')),
    db.Column('producto_id', db.Integer, ForeignKey('productos.id')),
    db.Column('cantidad', db.Integer)
)

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=True)
    habilitado = db.Column(db.Boolean, default=True) 
    facturas = relationship('Facturas', secondary=factura_producto, back_populates='productos')
    albaranes = relationship('Albaran', secondary=albaran_producto, back_populates='productos')

class Albaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    productos = relationship('Productos', secondary=albaran_producto, back_populates='albaranes')

class Facturas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    productos = relationship('Productos', secondary=factura_producto, back_populates='facturas')
