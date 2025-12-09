from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class DisciplineForm(FlaskForm):
    name = StringField('Назва дисципліни', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Опис', validators=[Length(max=500)])
    hours = IntegerField('Кількість годин', validators=[DataRequired()])
    
   
    category_id = SelectField('Категорія', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Зберегти')

class CategoryForm(FlaskForm):
    name = StringField('Назва категорії', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Зберегти')