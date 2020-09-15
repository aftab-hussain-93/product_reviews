from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField
from wtforms.validators import DataRequired


class ReviewField(FlaskForm):
	review = TextAreaField('Review', validators = [DataRequired(message='Review field is missing') ])
	rating = SelectField('Rating', choices = [('1',1), ('2',2), ('3', 3), ('4', 4), ('5', 5)])