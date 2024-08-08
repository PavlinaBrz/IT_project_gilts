import pandas as pd
from sqlalchemy import create_engine


def load_data_to_db(file_path, db_url):
    # Načtení dat z Excel souboru
    df = pd.read_excel(file_path)

    # Vytvoření připojení k databázi
    engine = create_engine(db_url)

    # Uložení dat do databáze
    df.to_sql('animals', con=engine, if_exists='replace', index=False)


# Volání funkce s cestou k Excel souboru a URL databáze
load_data_to_db('data_projekt.xlsx', 'sqlite:///instance/database_gilts.db')
