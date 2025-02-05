"""
db.py
-----
Tento modul inicializuje instanci SQLAlchemy, kterou používají ostatní části aplikace.
Veškeré modely (třídy) a databázové operace jsou vázány na objekt `db` z tohoto souboru.
"""

from flask_sqlalchemy import SQLAlchemy

#: Vytvoření instance SQLAlchemy, kterou budou využívat modely a další moduly
db = SQLAlchemy()