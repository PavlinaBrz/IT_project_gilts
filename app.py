"""
app.py
------
Tento modul definuje hlavní Flask aplikaci pro evidenci prasniček (registrace a přihlašování uživatelů,
přidávání a editace zvířat, zobrazování růstové křivky, apod.).

Běžně se spouští přímo (python app.py) a využívá nastavení v configu:
    - SQLAlchemy pro práci s DB
    - WTForms pro validaci formulářů
    - Flask-Login pro autentizaci
"""

import os
import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_wtf.csrf import CSRFProtect
import matplotlib
matplotlib.use('Agg')       # Nastavení backendu před importem pyplot
from matplotlib import pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm, AnimalForm
from database_users import add_user, get_user, User
from database_animal import Animals
from db import db
from io import BytesIO
from datetime import datetime
from flask_migrate import Migrate
import base64

#: Vytvoření instance Flask aplikace
app = Flask(__name__)

#: Cesta k SQLite databázi v podadresáři "instance"
db_path = os.path.join(os.path.abspath(os.getcwd()), "instance", "database_gilts.db")
db_path = db_path.replace("\\", "/")
print("DB PATH:", db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#: Nastavení tajného klíče pro Flask session a CSRF
app.config['SECRET_KEY'] = os.urandom(24)

#: Inicializace SQLAlchemy a migrací
db.init_app(app)
migrate = Migrate(app, db)

#: Zapnutí ochrany proti CSRF
csrf = CSRFProtect(app)

#: Nastavení Flask-Login manageru
login_manager = LoginManager()
login_manager.init_app(app)
#: URL endpoint, kam se uživatel přesměruje, pokud není přihlášen
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    Funkce pro načtení uživatele do Flask-Login.
    Používá se při ověřování session, vrací instanci User (nebo None).

    :param user_id: Primární klíč uživatele (id)
    :return: Instance User nebo None.
    """
    return db.session.get(User, int(user_id))


@app.route('/')
@login_required
def index():
    """
    Hlavní (domovská) stránka aplikace.
    Vyžaduje přihlášení - pokud uživatel není přihlášen, přesměruje se na /login.

    :return: Rendrovaná šablona 'index.html'
    """
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Stránka pro registraci uživatele s formulářem (RegistrationForm).
    - Při GET zobrazí formulář k vyplnění.
    - Při POST ověří validitu, vytvoří nového uživatele (pokud neexistuje)
      a přesměruje na /login. V opačném případě zobrazí chybu.

    :return: Rendrovaná šablona 'register.html'
             buď prázdný formulář (GET) nebo při chybách validace
             Při úspěchu redirect na /login.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Registration form validated successfully.")
        existing_user = get_user(form.username.data)
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('register.html', form=form)
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        add_user(form.username.data, hashed_password)
        print(f"Stored password hash during registration: {hashed_password}")
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    else:
        print("Registration form validation failed.")
        print(form.errors)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Stránka pro přihlášení uživatele (LoginForm).
    - Při GET zobrazí formulář.
    - Při POST validuje data, ověří heslo v DB a při úspěchu provede login_user().

    :return: Rendrovaná šablona 'login.html'
             nebo redirect na '/' při úspěšném přihlášení.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.username.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
            return render_template('login.html', form=form)
    else:
        if request.method == 'POST':
            # Log the form errors if the method is POST and validation failed
            print("Login form validation failed.")
            print(form.errors)
        return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Odhlášení uživatele.
    - Zavolá logout_user() a přesměruje na /login s informační hláškou.

    :return: Redirect na /login
    """
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/animals')
@login_required
def animals():
    """
    Stránka zobrazující seznam zvířat (paginovaný).
    - Načte z DB (model Animals), 20 záznamů na stránku.
    - Parametr 'page' určuje stránku.

    :return: Rendrovaná šablona 'animals.html' s listem zvířat (animals).
    """
    page = request.args.get('page', 1, type=int)
    filter_id = request.args.get('kratke_ID', type=int)
    if filter_id:
        query = Animals.query.filter_by(kratke_ID=filter_id)
    else:
        query = Animals.query
    animals_paginated = query.paginate(page=page, per_page=20)
    print("Záznamy v databázi:", [animal for animal in animals_paginated.items])  # Debugging
    # Předávám se celý paginovaný objekt, aby byly dostupné atributy has_prev, next_num, atd.
    return render_template('animals.html', animals=animals_paginated)


@app.route('/add_animal', methods=['GET', 'POST'])
@login_required
def add_animal():
    """
    Stránka pro přidání nového zvířete (AnimalForm).
    - Při GET zobrazí prázdný formulář.
    - Při POST validuje a uloží nový záznam do DB (model Animals).
      Pokud uspěje, přesměruje na /animals s hláškou.

    :return: Rendrovaná šablona 'add_animal.html' nebo redirect na /animals
    """
    form = AnimalForm()
    if form.validate_on_submit():
        print("Formulář validní:", form.data)
        try:
            new_animal = Animals(
                kratke_ID=form.kratke_ID.data,
                datum_vazeni_I=form.datum_vazeni_I.data,
                tyden_vazeni_I=form.tyden_vazeni_I.data,
                hmotnost_I=form.hmotnost_I.data,
                datum_vazeni_II=form.datum_vazeni_II.data,
                tyden_vazeni_II=form.tyden_vazeni_II.data,
                hmotnost_II=form.hmotnost_II.data,
                datum_vazeni_III=form.datum_vazeni_III.data,
                tyden_vazeni_III=form.tyden_vazeni_III.data,
                hmotnost_III=form.hmotnost_III.data,
                turnus=form.turnus.data,
                rok=form.rok.data,
                interni_ID=form.interni_ID.data,
                ID=form.ID.data,
                datum_narozeni=form.datum_narozeni.data,
                datum_spek=form.datum_spek.data,
                tyden_spek=form.tyden_spek.data,
                spek=form.spek.data,
                rije=form.rije.data
            )
            db.session.add(new_animal)
            db.session.commit()
            print(f'Záznam úspěšně přidán: {new_animal}')
            flash('Zvíře bylo úspěšně přidáno!', 'success')
            return redirect(url_for('animals'))
        except Exception as e:
            print("Chyba při ukládání do databáze:", e)
            db.session.rollback()
            flash(f'Nastala chyba při přidávání zvířete: {e}', 'danger')
    else:
        # Pokud je metoda GET nebo formulář neprošel validací, jednoduše vykreslíme formulář.
        if request.method == 'POST':
            print("Formulář neprošel validací:", form.errors)
    return render_template('add_animal.html', form=form)


@app.route('/edit_animal/<int:kratke_ID>', methods=['GET', 'POST'])
@login_required
def edit_animal(kratke_ID):
    """
    Stránka pro úpravu stávajícího zvířete.
    - Parametr kratke_ID určuje záznam v DB, pokud neexistuje, vrací 404.
    - Při GET se formulář předvyplní stávajícími hodnotami.
    - Při POST se ověří validita formuláře a podle toho se sloupce updatují.

    :param kratke_ID: Primární klíč zvířete (model Animals)
    :return: Rendrovaná šablona 'edit_animal.html' nebo redirect na /animals
    """
    print(f"Načítám záznam podle krátké ID: {kratke_ID}")
    animal = Animals.query.get_or_404(kratke_ID)
    print(f"Načtený záznam: {animal}")
    form = AnimalForm(obj=animal)
    if form.validate_on_submit():
        print("Formulář byl odeslán a je validní.")
        try:
            # Update jen to, co není None
            if form.kratke_ID.data is not None:
                animal.kratke_ID = form.kratke_ID.data
            if form.datum_vazeni_I.data is not None:
                animal.datum_vazeni_I = form.datum_vazeni_I.data
            if form.tyden_vazeni_I.data is not None:
                animal.tyden_vazeni_I = form.tyden_vazeni_I.data
            if form.hmotnost_I.data is not None:
                animal.hmotnost_I = form.hmotnost_I.data
            if form.datum_vazeni_II.data is not None:
                animal.datum_vazeni_II = form.datum_vazeni_II.data
            if form.tyden_vazeni_II.data is not None:
                animal.tyden_vazeni_II = form.tyden_vazeni_II.data
            if form.hmotnost_II.data is not None:
                animal.hmotnost_II = form.hmotnost_II.data
            if form.datum_vazeni_III.data is not None:
                animal.datum_vazeni_III = form.datum_vazeni_III.data
            if form.tyden_vazeni_III.data is not None:
                animal.tyden_vazeni_III = form.tyden_vazeni_III.data
            if form.hmotnost_III.data is not None:
                animal.hmotnost_III = form.hmotnost_III.data
            if form.turnus.data is not None:
                animal.turnus = form.turnus.data
            if form.rok.data is not None:
                animal.rok = form.rok.data
            if form.interni_ID.data is not None:
                animal.interni_ID = form.interni_ID.data
            if form.ID.data is not None:
                animal.ID = form.ID.data
            if form.datum_narozeni.data is not None:
                animal.datum_narozeni = form.datum_narozeni.data
            if form.datum_spek.data is not None:
                animal.datum_spek = form.datum_spek.data
            if form.tyden_spek.data is not None:
                animal.tyden_spek = form.tyden_spek.data
            if form.spek.data is not None:
                animal.spek = form.spek.data
            if form.rije.data is not None:
                animal.rije = form.rije.data

            db.session.commit()
            flash('Záznam byl úspěšně upraven!', 'success')
            return redirect(url_for('animals'))
        except Exception as e:
            db.session.rollback()
            flash(f'Nastala chyba při ukládání změn: {e}', 'danger')
        """if form.errors:
            print("Formulář neprošel validací:", form.errors)
"""
    return render_template('edit_animal.html', form=form, animal=animal)


"""@app.template_filter('toinputformat')
def to_input_format(value):
    
    Custom filtr pro Jinja2, který konvertuje datetime na formát
    vhodný pro <input type="datetime-local"> (např. 'YYYY-MM-DDTHH:mm').

    :param value: Hodnota (datetime nebo string), která se má převést
    :return: String ve formátu 'YYYY-MM-DDTHH:MM' nebo prázdný string
    
    if value is None or value == '':
        return ''
    if isinstance(value, str):
        # Try to parse the string into a datetime object
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    return value.strftime('%Y-%m-%dT%H:%M')"""


@app.route('/delete_animal/<int:kratke_ID>', methods=['POST'])
@login_required
def delete_animal(kratke_ID):
    animal = Animals.query.get_or_404(kratke_ID)
    try:
        db.session.delete(animal)
        db.session.commit()
        flash(f'Záznam s krátkým ID {kratke_ID} byl úspěšně smazán!', 'succes')
    except Exception as e:
        db.session.rollback()
        flash(f'Nastala chyba při mazání záznamu: {e}', 'danger')
    return redirect(url_for('animals'))


@app.route('/growth_curve')
@login_required
def growth_curve():
    """
    Generuje graf růstové křivky jako PNG obrázek.
    - Projdou se záznamy zvířat, rozdělí se na vážení I, II, III.
    - Vyrobí se DataFrame pro každé vážení, spočítá průměr hmotnosti za týden
    - Vykreslí se do matplotlib grafu a vrátí se binární PNG (send_file).

    :return: PNG obrázek s MIME 'image/png'
    """

    # Volitelné filtrovací GET parametry (turnus a rok)

    turnus_filter = request.args.get('turnus', type=int)
    rok_filter = request.args.get('rok', type=int)

    # Upravený dotaz - pokud je filtr zadán, přidáme podmínky
    query = Animals.query.filter(Animals.datum_narozeni.isnot(None))
    if turnus_filter is not None:
        query = query.filter(Animals.turnus == turnus_filter)
    if rok_filter is not None:
        query = query.filter(Animals.rok == rok_filter)

    animals = query.all()

    data_I = []
    data_II = []
    data_III = []

    # Naplnění seznamů pro 3 vážení
    for animal in animals:
        if animal.datum_vazeni_I and animal.hmotnost_I:
            age_weeks_I = (animal.datum_vazeni_I - animal.datum_narozeni).days / 7
            data_I.append((age_weeks_I, animal.hmotnost_I))
        if animal.datum_vazeni_II and animal.hmotnost_II:
            age_weeks_II = (animal.datum_vazeni_II - animal.datum_narozeni).days / 7
            data_II.append((age_weeks_II, animal.hmotnost_II))
        if animal.datum_vazeni_III and animal.hmotnost_III:
            age_weeks_III = (animal.datum_vazeni_III - animal.datum_narozeni).days / 7
            data_III.append((age_weeks_III, animal.hmotnost_III))

    # Vytvoření DataFrame pro každé vážení
    df_I = pd.DataFrame(data_I, columns=['age_weeks', 'weight']) if data_I else pd.DataFrame(
        columns=['age_weeks', 'weight'])
    df_II = pd.DataFrame(data_II, columns=['age_weeks', 'weight']) if data_II else pd.DataFrame(
        columns=['age_weeks', 'weight'])
    df_III = pd.DataFrame(data_III, columns=['age_weeks', 'weight']) if data_III else pd.DataFrame(
        columns=['age_weeks', 'weight'])

    # Zaokrouhlení na celé týdny a groupby průměr
    if not df_I.empty:
        df_I['week'] = df_I['age_weeks'].round(0).astype(int)
        avg_I = df_I.groupby('week')['weight'].mean().reset_index()
    else:
        avg_I = pd.DataFrame(columns=['weeks', 'weight'])

    if not df_II.empty:
        df_II['week'] = df_II['age_weeks'].round(0).astype(int)
        avg_II = df_II.groupby('week')['weight'].mean().reset_index()
    else:
        avg_II = pd.DataFrame(columns=['weeks', 'weight'])

    if not df_III.empty:
        df_III['week'] = df_III['age_weeks'].round(0).astype(int)
        avg_III = df_III.groupby('week')['weight'].mean().reset_index()
    else:
        avg_III = pd.DataFrame(columns=['weeks', 'weight'])

    # Vykreslení grafu
    fig, ax = plt.subplots(1, 1)

    if not avg_I.empty:
        ax.plot(avg_I['week'], avg_I['weight'], label='Vážení I – průměr', marker='o')
    if not avg_II.empty:
        ax.plot(avg_II['week'], avg_II['weight'], label='Vážení II – průměr', marker='o')
    if not avg_III.empty:
        ax.plot(avg_III['week'], avg_III['weight'], label='Vážení III – průměr', marker='o')

    # Referenční křivka
    reference_weeks = list(range(1, 41))
    reference_weights = [
        1.5, 2.5, 4.0, 5.5, 7.0, 8.5, 10.0, 12.0, 14.0, 16.0,
        18.0, 20.0, 22.5, 25.0, 27.5, 30.0, 33.0, 36.0, 39.0, 42.0,
        45.0, 48.0, 51.0, 54.0, 57.0, 60.0, 63.0, 66.0, 69.0, 72.0,
        75.0, 78.0, 81.0, 84.0, 87.0, 90.0, 93.0, 96.0, 99.0, 102.0
    ]
    ax.plot(reference_weeks, reference_weights, linestyle='--', label='Referenční křivka')

    ax.set_xlabel('Stáří (týdny)')
    ax.set_ylabel('Hmotnost (kg)')
    ax.set_title('Růstová křivka – průměry zaokrouhlených týdnů')
    ax.legend()

    # Uložíme graf do paměti a zakódujeme jej do base64
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)  # Zavřeme figurku, abychom uvolnili zdroje

    img_b64 = base64.b64encode(img.getvalue()).decode('utf8')
    print("Délka base64 řetězce:", len(img_b64))

    return render_template('growth_curve.html', image=img_b64, turnus_filter=turnus_filter, rok_filter=rok_filter)


"""def weight_function(age_weeks):
    
    Jednoduchá matematická funkce pro výpočet hmotnosti z věku v týdnech.
    Slouží jako příklad, jak by mohla vypadat predikce hmotnosti.

    :param age_weeks: Věk zvířete v týdnech (float nebo int).
    :return: Odhad hmotnosti (float).
    
    return 2.5 * age_weeks + 3"""


if __name__ == '__main__':
    # Pro produkci použít například Gunicorn: gunicorn -w 4 app:app
    app.run(debug=True)
