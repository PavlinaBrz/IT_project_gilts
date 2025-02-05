"""
database_animal.py
------------------
Tento modul obsahuje definici SQLAlchemy modelu 'Animals' a několik pomocných funkcí
pro práci s touto tabulkou v databázi (přidávání nových záznamů, získání seznamu,
aktualizace existujících záznamů).
"""

from flask_sqlalchemy import SQLAlchemy
from db import db  # Importuje instanci SQLAlchemy ze souboru `db.py`


class Animals(db.Model):
    """
    SQLAlchemy model reprezentující tabulku 'animals' v databázi.

    Obsahuje údaje o prasničkách a jejich vážení (datum a hmotnost),
    včetně poloh s názvy 'I', 'II', 'III' pro více vážení.
    Povinné sloupce: kratke_ID (PK), turnus, rok, interni_ID, ID
    Nepovinné sloupce: datum_vazeni_x, hmotnost_x, atd.
    """
    __tablename__ = 'animals'  # Název tabulky v databázi

    kratke_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    datum_vazeni_I = db.Column(db.Date, nullable=True)
    tyden_vazeni_I = db.Column(db.Integer, nullable=True)
    hmotnost_I = db.Column(db.Float, nullable=True)
    datum_vazeni_II = db.Column(db.Date, nullable=True)
    tyden_vazeni_II = db.Column(db.Integer, nullable=True)
    hmotnost_II = db.Column(db.Float, nullable=True)
    datum_vazeni_III = db.Column(db.Date, nullable=True)
    tyden_vazeni_III = db.Column(db.Integer, nullable=True)
    hmotnost_III = db.Column(db.Float, nullable=True)
    turnus = db.Column(db.Integer, nullable=True)
    rok = db.Column(db.Integer, nullable=True)
    interni_ID = db.Column(db.Integer, nullable=True)
    ID = db.Column(db.Integer, nullable=True)
    datum_narozeni = db.Column(db.Date, nullable=True)
    datum_spek = db.Column(db.Date, nullable=True)
    tyden_spek = db.Column(db.Integer, nullable=True)
    spek = db.Column(db.Float, nullable=True)
    rije = db.Column(db.Date, nullable=True)

    def __repr__(self):
        """
        Textová reprezentace objektu Animals,
        vypisuje základní atributy (kratke_ID, datumy a váhy, turnus, atd.)
        """
        return (f'<Animals {self.kratke_ID}, {self.datum_vazeni_I}, {self.tyden_vazeni_I}, {self.hmotnost_I},'
                f'{self.datum_vazeni_II}, {self.tyden_vazeni_II}, {self.hmotnost_II}, {self.datum_vazeni_III},'
                f'{self.tyden_vazeni_III}, {self.hmotnost_III}, {self.turnus}, {self.rok}, {self.interni_ID},'
                f'{self.ID}, {self.datum_narozeni}, {self.datum_spek}, {self.tyden_spek}, {self.spek},'
                f'{self.rije}>')


def add_animal(kratke_ID, datum_vazeni_I, tyden_vazeni_I, hmotnost_I,
               datum_vazeni_II, tyden_vazeni_II, hmotnost_II,
               datum_vazeni_III, tyden_vazeni_III, hmotnost_III,
               turnus, rok, interni_ID, ID, datum_narozeni, datum_spek,
               tyden_spek, spek, rije):
    """
    Vytvoří nový záznam (Animals) v databázi s předanými hodnotami
    a uloží ho pomocí db.session.commit().

    :param kratke_ID: Jedinečný primární klíč
    :param datum_vazeni_I: Datum prvního vážení
    :param tyden_vazeni_I: Týden prvního vážení
    :param hmotnost_I: Hmotnost při prvním vážení
    :param datum_vazeni_II: Datum druhého vážení
    :param tyden_vazeni_II: Týden druhého vážení
    :param hmotnost_II: Hmotnost při druhém vážení
    :param datum_vazeni_III: Datum třetího vážení
    :param tyden_vazeni_III: Týden třetího vážení
    :param hmotnost_III: Hmotnost při třetím vážení
    :param turnus: Číslo turnusu
    :param rok: Rok turnusu
    :param interni_ID: Interní ID prasničky
    :param ID: Další ID (např. vnější identifikace)
    :param datum_narozeni: Datum narození
    :param datum_spek: Datum měření špeku
    :param tyden_spek: Týden měření špeku
    :param spek: Tloušťka špeku (float)
    :param rije: Datum říje
    :return: None
    """
    new_animal = Animals(
        kratke_ID=kratke_ID,
        datum_vazeni_I=datum_vazeni_I,
        tyden_vazeni_I=tyden_vazeni_I,
        hmotnost_I=hmotnost_I,
        datum_vazeni_II=datum_vazeni_II,
        tyden_vazeni_II=tyden_vazeni_II,
        hmotnost_II=hmotnost_II,
        datum_vazeni_III=datum_vazeni_III,
        tyden_vazeni_III=tyden_vazeni_III,
        hmotnost_III=hmotnost_III,
        turnus=turnus,
        rok=rok,
        interni_ID=interni_ID,
        ID=ID,
        datum_narozeni=datum_narozeni,
        datum_spek=datum_spek,
        tyden_spek=tyden_spek,
        spek=spek,
        rije=rije
    )
    db.session.add(new_animal)
    db.session.commit()
    print(f"Animal added: kratke_ID{kratke_ID}, datum_vazeni_I{datum_vazeni_I}, tyden_vazeni_I{tyden_vazeni_I},"
          f"hmotnost_I{hmotnost_I}, datum_vazeni_II{datum_vazeni_II}, tyden_vazeni_II{tyden_vazeni_II},"
          f"hmotnost_II{hmotnost_II}, datum_vazeni_III{datum_vazeni_III}, tyden_vazeni_III{tyden_vazeni_III},"
          f"hmotnost_III{hmotnost_III}, turnus{turnus}, rok{rok}, interni_ID{interni_ID}, ID{ID},"
          f"datum_narozeni{datum_narozeni}, datum_spek{datum_spek}, tyden_spek{tyden_spek}, spek{spek}, rije{rije}")


def get_animals():
    """
    Vrátí všechny záznamy tabulky 'animals' jako list instancí Animals.

    :return: List[Animals]
    """
    return Animals.query.all()


def update_animal(kratke_ID, datum_vazeni_I, tyden_vazeni_I, hmotnost_I,
                  datum_vazeni_II, tyden_vazeni_II, hmotnost_II,
                  datum_vazeni_III, tyden_vazeni_III, hmotnost_III,
                  turnus, rok, interni_ID, ID, datum_narozeni,
                  datum_spek, tyden_spek, spek, rije):
    """
    Provede update existujícího záznamu v tabulce Animals podle kratke_ID.
    Pokud záznam existuje, nastaví mu nové hodnoty a uloží do DB.

    :param kratke_ID: Primární klíč (int), slouží k vyhledání záznamu
    :param datum_vazeni_I: Datum prvního vážení
    :param tyden_vazeni_I: Týden prvního vážení
    :param hmotnost_I: Hmotnost při prvním vážení
    :param datum_vazeni_II: Datum druhého vážení
    :param tyden_vazeni_II: Týden druhého vážení
    :param hmotnost_II: Hmotnost při druhém vážení
    :param datum_vazeni_III: Datum třetího vážení
    :param tyden_vazeni_III: Týden třetího vážení
    :param hmotnost_III: Hmotnost při třetím vážení
    :param turnus: Číslo turnusu
    :param rok: Rok turnusu
    :param interni_ID: Interní ID prasničky
    :param ID: Další ID (např. vnější identifikace)
    :param datum_narozeni: Datum narození
    :param datum_spek: Datum měření špeku
    :param tyden_spek: Týden měření špeku
    :param spek: Tloušťka špeku (float)
    :param rije: Datum říje
    :return: Objekt Animals po úpravě, nebo None, pokud záznam neexistoval.
    """
    animal = Animals.query.get(kratke_ID)
    if animal:
        animal.kratke_ID = kratke_ID
        animal.datum_vazeni_I = datum_vazeni_I
        animal.tyden_vazeni_I = tyden_vazeni_I
        animal.hmotnost_I = hmotnost_I
        animal.datum_vazeni_II = datum_vazeni_II
        animal.tyden_vazeni_II = tyden_vazeni_II
        animal.hmotnost_II = hmotnost_II
        animal.datum_vazeni_III = datum_vazeni_III
        animal.tyden_vazeni_III = tyden_vazeni_III
        animal.hmotnost_III = hmotnost_III
        animal.turnus = turnus
        animal.rok = rok
        animal.interni_ID = interni_ID
        animal.ID = ID
        animal.datum_narozeni = datum_narozeni
        animal.datum_spek = datum_spek
        animal.tyden_spek = tyden_spek
        animal.spek = spek
        animal.rije = rije

        db.session.commit()
        print(
            f"Animal updated: kratke_ID{kratke_ID}, datum_vazeni_I{datum_vazeni_I}, tyden_vazeni_I{tyden_vazeni_I},"
            f"hmotnost_I{hmotnost_I}, datum_vazeni_II{datum_vazeni_II}, tyden_vazeni_II{tyden_vazeni_II},"
            f"hmotnost_II{hmotnost_II}, datum_vazeni_III{datum_vazeni_III}, tyden_vazeni_III{tyden_vazeni_III},"
            f"hmotnost_III{hmotnost_III}, turnus{turnus}, rok{rok}, interni_ID{interni_ID}, ID{ID},"
            f"datum_narozeni{datum_narozeni}, datum_spek{datum_spek}, tyden_spek{tyden_spek}, spek{spek}, rije{rije}")
        return animal
    return None

