from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AnimalForm(FlaskForm):
    kratke_ID = IntegerField('kratke_ID', validators=[DataRequired(), NumberRange(min=0)])
    turnus = IntegerField('turnus', validators=[DataRequired(), NumberRange(min=0)])
    rok = StringField('rok', validators=[DataRequired(), Length(min=1, max=80)])
    interni_ID = IntegerField('interni_ID', validators=[DataRequired(), NumberRange(min=0)])
    ID = IntegerField('ID', validators=[DataRequired(), NumberRange(min=0)])
    datum_narozeni = DateField('datum_narozeni', validators=[DataRequired(), NumberRange(min=0)])
    datum_vazeni = DateField('datum_vazeni', validators=[DataRequired(), NumberRange(min=0)])
    tyden_vazeni = IntegerField('tyden_vazeni', validators=[DataRequired(), NumberRange(min=0)])
    hmotnost = FloatField('hmotnost', validators=[DataRequired(), NumberRange(min=0)])
    datum_spek = DateField('datum_spek', validators=[DataRequired(), NumberRange(min=0)])
    tyden_spek = IntegerField('tyden_spek', validators=[DataRequired(), NumberRange(min=0)])
    spek = FloatField('spek', validators=[DataRequired(), Length(min=1, max=80)])
    rije = DateField('rije', validators=[DataRequired(), NumberRange(min=0)])
