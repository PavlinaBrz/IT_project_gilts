"""
load_data.py
------------
Tento modul se stará o načtení dat z Excel souboru (např. 'data_projekt.xlsx')
a jejich uložení do tabulky 'animals' v SQLite databázi.
Volá se obvykle samostatně (python load_data.py), čímž dojde k importu.

Po úspěšném importu lze v konzoli vidět, kolik záznamů je v tabulce `animals`.
Pokud se objeví chyba (např. chybějící sloupce), vše se vypíše do terminálu.
"""

import os
import pandas as pd
from app import app  # Import aplikace Flask
from database_animal import Animals  # Import modelu tabulky
from sqlalchemy import create_engine


# Volitelný tisk obsahu tabulky animals (jen pro kontrolu)
with app.app_context():
    print("Aktuální záznamy v tabulce 'animals':", Animals.query.all())


def load_data_to_database(file_path, db_path):
    """
    Funkce pro načtení dat z Excelu a jejich uložení do tabulky 'animals' v SQLite databázi.

    1) Pomocí pandas se načte Excel (header=1 → druhý řádek je záhlaví).
    2) Zkontrolují a přejmenují se sloupce, vyplní se výchozí hodnoty.
    3) Datumové sloupce se zkonvertují tak, aby obsahovaly jen DATE (bez času).
    4) Data se zapíší do tabulky 'animals' (df.to_sql).
    5) Volitelně se provede kontrola, kolik záznamů je teď v DB.

    :param file_path: Cesta k Excel souboru (např. 'data_projekt.xlsx').
    :param db_path: Cesta k databázovému souboru (např. 'C:/.../instance/database_gilts.db').
    :raises ValueError: Pokud chybí některé požadované sloupce.
    :return: None
    """
    engine = create_engine(f"sqlite:///{db_path}")

    try:
        # 1) Načtení dat z Excelu
        df = pd.read_excel(file_path, header=1)

        # 2) Přejmenování sloupců, pokud se nenačetly správně
        df.columns = [
            'kratke_ID', 'datum_vazeni_I', 'tyden_vazeni_I', 'hmotnost_I',
            'datum_vazeni_II', 'tyden_vazeni_II', 'hmotnost_II',
            'datum_vazeni_III', 'tyden_vazeni_III', 'hmotnost_III',
            'turnus', 'rok', 'interni_ID', 'ID', 'datum_narozeni',
            'datum_spek', 'tyden_spek', 'spek', 'rije'
        ]

        # 3) Nahradíme prázdné hodnoty ve sloupcích výchozími hodnotami
        default_values = {
            'kratke_ID': 0,
            'datum_vazeni_I': pd.NaT,
            'tyden_vazeni_I': 0,
            'hmotnost_I': 0.0,
            'datum_vazeni_II': pd.NaT,
            'tyden_vazeni_II': 0,
            'hmotnost_II': 0.0,
            'datum_vazeni_III': pd.NaT,
            'tyden_vazeni_III': 0,
            'hmotnost_III': 0.0,
            'turnus': 0,
            'rok': 0,
            'interni_ID': 0,
            'ID': 0,
            'datum_narozeni': pd.NaT,
            'datum_spek': pd.NaT,
            'tyden_spek': 0,
            'spek': 0.0,
            'rije': pd.NaT,
        }
        df.fillna(value=default_values, inplace=True)

        # 4) U sloupců, které mají být jen DATE (bez času), ořízneme čas
        date_cols = [
            'datum_vazeni_I',
            'datum_vazeni_II',
            'datum_vazeni_III',
            'datum_narozeni',
            'datum_spek',
            'rije'
        ]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

        # 5) Kontrola požadovaných sloupců
        required_columns = list(default_values.keys())
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Chybí požadované sloupce: {', '.join(missing_columns)}")

        # 6) Import dat do tabulky 'animals'
        try:
            print("DEBUG: Před to_sql df shape:", df.shape)
            df.to_sql('animals', con=engine, if_exists='append', index=False)
            print("DEBUG: Po to_sql")
            print("Data byla úspěšně importována.")

            # Volitelná kontrola v tom samém skriptu:
            with app.app_context():
                all_rows = Animals.query.all()
                print("Kontrola - počet záznamů:", len(all_rows))

        except Exception as e:
            print("Chyba při df.to_sql:", e)

    except Exception as e:
        print(f"Chyba při importu dat: {e}")


if __name__ == "__main__":
    # Pokud se skript spustí přímo, použijeme cesty jako v app.py
    db_path = os.path.join(os.path.abspath(os.getcwd()), "instance", "database_gilts.db")
    print("load_data DB PATH:", db_path)
    load_data_to_database("data_projekt.xlsx", db_path)