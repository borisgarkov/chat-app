from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=20)]
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=20)]
    )


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=20)]
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=20)]
    )

    password2 = PasswordField(
        validators=[InputRequired(), Length(min=2, max=20)]
    )
