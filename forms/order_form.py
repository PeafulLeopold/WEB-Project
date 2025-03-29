from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    submit = SubmitField('Оформить заказ')
