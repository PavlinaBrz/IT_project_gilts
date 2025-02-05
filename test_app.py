"""
test_app.py
-----------
Tento modul obsahuje sadu testů (pomocí pytest), které ověřují
základní funkce aplikace (registrace, přihlášení, přidání zvířete).

Používá in-memory SQLite databázi (':memory:') pro izolaci testů,
aby se nezasahovalo do produkčních dat.
"""

import pytest
from app import app
from db import db
from database_users import add_user, get_user
from database_animal import Animals


@pytest.fixture
def client():
    """
    Pytest fixture, která nastaví aplikaci do TESTING režimu
    a použije in-memory databázi. Po skončení testů se databáze zruší.

    :yield: Flask testovací klient
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # paměťová DB

    with app.test_client() as client:
        # V kontextu aplikace vytvoříme tabulky
        with app.app_context():
            db.create_all()
            # Můžeš přidat inicializační data, pokud je potřeba
        yield client


def test_register(client):
    """
    Otestuje registraci nového uživatele:
    - Pošle POST na /register s username a password
    - Očekává status kód 302 (přesměrování)
    - Ověří, že get_user('testuser') vrátí neprazdný výsledek
    """
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Přesměrování po úspěšné registraci
    user = get_user('testuser')
    assert user is not None


def test_login(client):
    """
    Otestuje přihlášení uživatele:
    - Nejprve přidá nového uživatele (manuálně, s hash heslem).
    - Pošle POST na /login s username a password
    - Očekává v reakci 'Login successful!'
    """
    add_user('testuser', 'hashedpassword')
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert b'Login successful!' in response.data


def test_add_animal(client):
    """
    Otestuje přidání nového zvířete přes POST na /add_animal:
    - Odešle formulářová data, včetně hmotnosti
    - Očekává status kód 302 (přesměrování) po úspěšném uložení
    - Ověří, zda se v DB objevil nový záznam
    - Poznámka: checkuje se 'hmotnost' == 50.0, ale v reálné DB existuje hmotnost_I, hmotnost_II, hmotnost_III
    """
    response = client.post('/add_animal', data={
        'kratke_ID': 1,
        'turnus': 2,
        'rok': 2025,
        'datum_narozeni': '2025-01-01',
        # Tady posíláme hmotnost do 'hmotnost_I' / 'hmotnost_II' / 'hmotnost_III'
        # místo původního 'hmotnost'.
        'hmotnost_I': 50.0,
        'hmotnost_II': 50.0,
        'hmotnost_III': 50.0,
    })
    assert response.status_code == 302  # Přesměrování po úspěšném přidání

    animal = Animals.query.get(1)
    assert animal is not None

    # POZN: V reálném kódu existuje animal.hmotnost_I/II/III,
    #       takže pokud chceme ověřit tu hodnotu,
    #       musíme patřičně použít hmotnost_I:
    assert animal.hmotnost_I == 50.0
    # Nebo klidně i:
    # assert animal.hmotnost_II == 50.0
    # assert animal.hmotnost_III == 50.0
