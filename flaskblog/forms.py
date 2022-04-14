from flask_wtf import FlaskForm #flask extension
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired #data required validator

#write python classes, converted into html form
#fit in template

class PostForm(FlaskForm): #inherit
    title = StringField('Subject', validators=[DataRequired()]) #(name of the field) label
    content = TextAreaField('Content', validators=[DataRequired()]) #DataRequired makes sure field isn't empty
    submit = SubmitField('Post') #submit button

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])                    
    submit = SubmitField('Comment') #submit button