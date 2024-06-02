from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class AlbaranForm(FlaskForm):
    nom1 = StringField("Nombre1", validators=[Length(min=1, max=50)])
    cantidad1 = IntegerField("Cantidad1", validators=[NumberRange(min=1)])
    nom2 = StringField("Nombre2", validators=[Length(min=1, max=50), Optional()])
    cantidad2 = IntegerField("Cantidad2", validators=[NumberRange(min=1), Optional()])
    nom3 = StringField("Nombre3", validators=[Length(min=1, max=50), Optional()])
    cantidad3 = IntegerField("Cantidad3", validators=[NumberRange(min=1), Optional()])
    nom4 = StringField("Nombre4", validators=[Length(min=1, max=50), Optional()])
    cantidad4 = IntegerField("Cantidad4", validators=[NumberRange(min=1), Optional()])


class FacturaForm(FlaskForm):
    nom1 = StringField("Nombre 1", validators=[Length(min=1, max=50)])
    cantidad1 = IntegerField("Cantidad 1", validators=[NumberRange(min=1)])
    nom2 = StringField("Nombre 2", validators=[Length(min=1, max=50), Optional()])
    cantidad2 = IntegerField("Cantidad 2", validators=[NumberRange(min=1), Optional()])
    nom3 = StringField("Nombre 3", validators=[Length(min=1, max=50), Optional()])
    cantidad3 = IntegerField("Cantidad 3", validators=[NumberRange(min=1), Optional()])
    nom4 = StringField("Nombre 4", validators=[Length(min=1, max=50), Optional()])
    cantidad4 = IntegerField("Cantidad 4", validators=[NumberRange(min=1), Optional()])