"""
data_excel.py
-------------
Tento modul obsahuje SQLAlchemy model GrowthData a funkce související s růstovými daty prasniček.
Slouží jako příklad paralelní tabulky k `animals`, kde se mohou uchovávat hodnoty pro výpočet
růstové křivky atd.
"""

import pandas as pd
from db import db
from sqlalchemy import create_engine


class GrowthData(db.Model):
    """
    SQLAlchemy model pro tabulku 'growth_data', která uchovává
    růstová data (věk, hmotnost) a volitelně růstovou rychlost.

    Sloupce:
      - id (int, PK)
      - age (int): Věk zvířete v týdnech
      - weight (float): Hmotnost (kg)
      - growth_rate (float, nullable): Vypočtená rychlost růstu
    """
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    growth_rate = db.Column(db.Float, nullable=True)


def calculate_growth_curve():
    """
    Načte všechny záznamy z tabulky GrowthData, přepočítá 'growth_rate'
    (jako weight / age) a uloží nové hodnoty do DB.

    1. Vytvoří DataFrame (pandas) z dat GrowthData.
    2. Spočítá sloupec 'growth_rate'.
    3. Uloží zpět do DB pomocí session commit.

    :return: DataFrame s nově spočítanými sloupci (stejné řádky, navíc 'growth_rate').
    """
    growth_data = GrowthData.query.all()
    # Pro každou instanci vezmeme (age, weight) a uložíme do pandas DataFrame
    df = pd.DataFrame([(d.age, d.weight) for d in growth_data], columns=['age', 'weight'])

    # Vypočteme růstovou rychlost jako poměr weight/age
    df['growth_rate'] = df['weight'] / df['age']

    # Projdeme řádky DataFrame a naplníme growth_rate zpět do Python objektů
    for index, row in df.iterrows():
        growth_data[index].growth_rate = row['growth_rate']

    db.session.commit()
    return df


if __name__ == "__main__":
    """
    Pokud se modul spouští přímo (python data_excel.py),
    provede se testovací kód - načteme tabulku 'animals' z DB
    a vytiskneme ji. Slouží pro rychlou kontrolu, zda DB funguje.
    """
    engine = create_engine('sqlite:///instance/database_gilts.db')
    df = pd.read_sql('animals', engine)
    print(df)