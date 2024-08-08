import os
import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_wtf.csrf import CSRFProtect
from matplotlib import pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm
from database_users import add_user, get_user, User
from database_animal import Animals
from db import db
from io import BytesIO
from datetime import datetime


app = Flask(__name__)
db_path = os.path.join(os.path.abspath(os.getcwd()), "instance", "database_gilts.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Initialize the databases
with app.app_context():
    db.create_all()
    print("Database and tables created.")


@app.route('/')
@login_required
def index():
    # hlavní stránka aplikace, která vyžaduje přihlášení
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # stránka pro registraci uživatele s formulářem
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
    # stránka pro přihlášení uživatele s formulářem
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
    #Odhlášení uživatele a přesměrování na přihlašovací stránku.
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/animals')
@login_required
def animals():
    # stráka pro zobrazení všech zvířat uložených v databázi
    animals = Animals.query.all()
    for animal in animals:
        print(animal)
    return render_template('animals.html', animals=animals)


@app.route('/add_animal', methods=['GET', 'POST'])
@login_required
def add_animal():
    # stránka pro přidání nového zvířete do databáze s formulářem
    if request.method == 'POST':
        kratke_ID = request.form['kratke_ID']
        turnus = request.form['turnus']
        rok = request.form['rok']
        interni_ID = request.form['interni_ID']
        ID = request.form['ID']
        datum_narozeni = request.form['datum_narozeni']
        datum_vazeni = request.form['datum_vazeni']
        tyden_vazeni = request.form['tyden_vazeni']
        hmotnost = request.form['hmotnost']
        datum_spek = request.form['datum_spek']
        tyden_spek = request.form['tyden_spek']
        spek = request.form['spek']
        rije = request.form['rije']

        new_animal = Animals(
            kratke_ID=kratke_ID,
            turnus=turnus,
            rok=rok,
            interni_ID=interni_ID,
            ID=ID,
            datum_narozeni=datum_narozeni,
            datum_vazeni=datum_vazeni,
            tyden_vazeni=tyden_vazeni,
            hmotnost=hmotnost,
            datum_spek=datum_spek,
            tyden_spek=tyden_spek,
            spek=spek,
            rije=rije
        )

        db.session.add(new_animal)
        db.session.commit()
        flash('Animal added successfully!', 'success')
        return redirect(url_for('animals'))

    return render_template('add_animal.html')



@app.route('/edit_animal/<int:kratke_ID>', methods=['GET', 'POST'])
@login_required
def edit_animal(kratke_ID):
    #stránka pro úpravu existujícího zvířete v databázi
    animal = Animals.query.get_or_404(kratke_ID)
    if request.method == 'POST':
        animal.kratke_ID = request.form['kratke_ID']
        animal.turnus = request.form['turnus']
        animal.rok = request.form['rok']
        animal.interni_ID = request.form['interni_ID']
        animal.ID = request.form['ID']
        animal.datum_narozeni = datetime.strptime(request.form['datum_narozeni'], '%Y-%m-%dT%H:%M')
        animal.datum_vazeni = datetime.strptime(request.form['datum_vazeni'], '%Y-%m-%dT%H:%M')
        animal.tyden_vazeni = request.form['tyden_vazeni']
        animal.hmotnost = request.form['hmotnost']
        animal.datum_spek = datetime.strptime(request.form['datum_spek'], '%Y-%m-%dT%H:%M')
        animal.tyden_spek = request.form['tyden_spek']
        animal.spek = request.form['spek']
        animal.rije = datetime.strptime(request.form['rije'], '%Y-%m-%dT%H:%M')

        db.session.commit()
        flash('Animal updated successfully!', 'success')
        return redirect(url_for('animals'))

    return render_template('edit_animal.html', animal=animal)


@app.template_filter('toinputformat')
def to_input_format(value):
    # Filtr pro formátování datetime hodnot ve formulářích na stránkách.
    if value is None or value == '':
        return ''
    if isinstance(value, str):
        # Try to parse the string into a datetime object
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    return value.strftime('%Y-%m-%dT%H:%M')



@app.route('/growth_curve')
@login_required
def growth_curve():
    # Stránka pro vykreslení grafu růstové křivky zvířat na základě dat uložených v databázi.
    animals = Animals.query.filter(Animals.datum_narozeni.isnot(None), Animals.datum_vazeni.isnot(None),
                                  Animals.hmotnost.isnot(None)).all()

    # Calculate age in weeks and group weights by age in weeks
    age_weight = []
    for animal in animals:
        age_weeks = (animal.datum_vazeni - animal.datum_narozeni).days / 7
        age_weight.append((age_weeks, animal.hmotnost))

    # Create a DataFrame and calculate the average weight for each week
    df = pd.DataFrame(age_weight, columns=['Age (weeks)', 'Weight (kg)'])
    average_weights = df.groupby('Age (weeks)').agg({'Weight (kg)': 'mean', 'Age (weeks)': 'size'}).rename(
        columns={'Age (weeks)': 'Count'}).reset_index()

    # Reference growth curve
    reference_weeks = list(range(1, 41))
    reference_weights = [
        1.5, 2.5, 4.0, 5.5, 7.0, 8.5, 10.0, 12.0, 14.0, 16.0,
        18.0, 20.0, 22.5, 25.0, 27.5, 30.0, 33.0, 36.0, 39.0, 42.0,
        45.0, 48.0, 51.0, 54.0, 57.0, 60.0, 63.0, 66.0, 69.0, 72.0,
        75.0, 78.0, 81.0, 84.0, 87.0, 90.0, 93.0, 96.0, 99.0, 102.0
    ]

    # Plotting the growth curves
    fig, ax = plt.subplots()
    ax.plot(average_weights['Age (weeks)'], average_weights['Weight (kg)'], label='Average Weight per Week')
    ax.plot(reference_weeks, reference_weights, label='Reference Growth Curve', linestyle='--')
    ax.set_xlabel('Age (weeks)')

    # Add the count of animals to the ylabel
    total_animals = df['Age (weeks)'].count()
    ax.set_ylabel(f'Weight (kg) - Averaged from {total_animals} animals')

    ax.set_title('Growth Curve')
    ax.legend()

    # Save plot to a BytesIO object
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

def weight_function(age_weeks):
    # Jednoduchá matematická funkce pro výpočet hmotnosti na základě věku ve formátu týdnů.
    return 2.5 * age_weeks + 3


if __name__ == '__main__':
    app.run(debug=True)
