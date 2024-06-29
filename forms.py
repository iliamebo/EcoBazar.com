from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FileField, PasswordField, SearchField

class AddProduct(FlaskForm):
    name = StringField(label="name")
    file = FileField(label="file")
    price = IntegerField(label="price")
    category = SelectField(label="category")
    submit = SubmitField(label="submit")

class DeleteFromCartForm(FlaskForm):
    delete = SubmitField("Delete")

class SearchForm(FlaskForm):
    search = SearchField('search')


class RegisterForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    register = SubmitField(label="register")

class LoginForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    login = SubmitField(label="login")