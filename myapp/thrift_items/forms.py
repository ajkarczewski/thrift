from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ThriftItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    item_details = TextAreaField('Details', validators=[DataRequired()])
    submit = SubmitField('POST >')