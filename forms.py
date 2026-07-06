from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Ingresar")

class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Registrar")
