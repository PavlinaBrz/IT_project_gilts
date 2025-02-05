"""
forms.py
--------
Obsahuje definice WTForms formulářů pro uživatelskou registraci, přihlášení
a formulář pro zadávání údajů o zvířatech (AnimalForm).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
from datetime import date


class RegistrationForm(FlaskForm):
    """
    Formulář pro registraci nového uživatele.
    Využívá polí `username` a `password`, s validátory na délku, povinné vyplnění atd.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])


class LoginForm(FlaskForm):
    """
    Formulář pro přihlášení uživatele.
    Obsahuje políčka `username`, `password` a `submit` tlačítko.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AnimalForm(FlaskForm):
    """
    Formulář pro přidávání/editaci záznamů o prasničkách (tabulka Animals).
    U většiny polí je použit `Optional()` validátor (tj. nemusí být vyplněné).
    Políčka jako 'datum_narozeni' mají vlastní validaci (např. nemůže být budoucí).
    """
    kratke_ID = IntegerField('kratke_ID', validators=[DataRequired()], description="Jedinečné ID zvířete")
    datum_vazeni_I = DateField('Datum vážení I', format='%Y-%m-%d', validators=[Optional()])
    tyden_vazeni_I = IntegerField('Týden vážení I', validators=[Optional()])
    hmotnost_I = FloatField('Hmotnost I', validators=[Optional()])

    datum_vazeni_II = DateField('Datum vážení II', format='%Y-%m-%d', validators=[Optional()])
    tyden_vazeni_II = IntegerField('Týden vážení II', validators=[Optional()])
    hmotnost_II = FloatField('Hmotnost II', validators=[Optional()])

    datum_vazeni_III = DateField('Datum vážení III', format='%Y-%m-%d', validators=[Optional()])
    tyden_vazeni_III = IntegerField('Týden vážení III', validators=[Optional()])
    hmotnost_III = FloatField('Hmotnost III', validators=[Optional()])

    turnus = IntegerField('turnus', validators=[Optional()])
    rok = IntegerField('rok', validators=[Optional()], description="...")
    interni_ID = IntegerField('interni_ID', validators=[Optional(), NumberRange(min=0)], description="...")
    ID = IntegerField('ID', validators=[Optional(), NumberRange(min=0)], description="...")
    datum_narozeni = DateField('datum_narozeni', validators=[Optional()], description="...", format='%Y-%m-%d')
    def validate_datum_narozeni(self, field):
        """
        Vlastní validace pro datum narození. Zabraňuje zadání data v budoucnosti.
        """
        if field.data > date.today():
            raise ValidationError("Datum narození nemůže být v budoucnosti.")

    datum_spek = DateField('datum_spek', validators=[Optional()], description="...", format='%Y-%m-%d')
    tyden_spek = IntegerField('tyden_spek', validators=[Optional(), NumberRange(min=0)], description="...")
    spek = FloatField('spek', validators=[Optional()], description="...")
    rije = DateField('rije', validators=[Optional()], description="...", format='%Y-%m-%d')