from flask_sqlalchemy import SQLAlchemy
from db import db

class Animals(db.Model):
    __tablename__ = 'animals'
    kratke_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    turnus = db.Column(db.Integer)
    rok = db.Column(db.Text)
    interni_ID = db.Column(db.Integer, unique=True)
    ID = db.Column(db.Integer)
    datum_narozeni = db.Column(db.DateTime)
    datum_vazeni = db.Column(db.DateTime)
    tyden_vazeni = db.Column(db.Integer)
    hmotnost = db.Column(db.Float)
    datum_spek = db.Column(db.DateTime)
    tyden_spek = db.Column(db.Integer)
    spek = db.Column(db.Float)
    rije = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Animals {self.kratke_ID}, {self.turnus}, {self.rok}, {self.interni_ID}, {self.ID}, {self.datum_narozeni}, {self.datum_vazeni}, {self.tyden_vazeni}, {self.hmotnost}, {self.datum_spek}, {self.tyden_spek}, {self.spek}, {self.rije}>'


def add_animal(kratke_ID, turnus, rok, interni_ID, ID, datum_narozeni, datum_vazeni, tyden_vazeni, hmotnost, datum_spek, tyden_spek, spek, rije):
    new_animal = Animals(kratke_ID=kratke_ID, turnus=turnus, rok=rok, interni_ID=interni_ID, ID=ID, datum_narozeni=datum_narozeni, datum_vazeni=datum_vazeni, tyden_vazeni=tyden_vazeni, hmotnost=hmotnost, datum_spek=datum_spek, tyden_spek=tyden_spek, spek=spek, rije=rije)
    db.session.add(new_animal)
    db.session.commit()
    print(f"Animal added: kratke_ID{kratke_ID}, turnus{turnus}, rok{rok}, interni_ID{interni_ID}, ID{ID}, datum_narozeni{datum_narozeni}, datum_vazeni{datum_vazeni}, tyden_vazeni{tyden_vazeni}, hmotnost{hmotnost}, datum_spek{datum_spek}, tyden_spek{tyden_spek}, spek{spek}, rije{rije}")

def get_animals():
    return Animals.query.all()

def update_animal(kratke_ID, turnus, rok, interni_ID, ID, datum_narozeni, datum_vazeni, tyden_vazeni, hmotnost, datum_spek, tyden_spek, spek, rije):
    animal = Animals.query.get(kratke_ID)
    if animal:
        animal.kratke_ID = kratke_ID
        animal.turnus = turnus
        animal.rok = rok
        animal.interni_ID = interni_ID
        animal.ID = ID
        animal.datum_narozeni = datum_narozeni
        animal.datum_vazeni = datum_vazeni
        animal.tyden_vazeni = tyden_vazeni
        animal.hmotnost = hmotnost
        animal.datum_spek = datum_spek
        animal.tyden_spek = tyden_spek
        animal.spek = spek
        animal.rije = rije
        db.session.commit()
        print(f"Animal updated: kratke_ID{kratke_ID}, turnus{turnus}, rok{rok}, interni_ID{interni_ID}, ID{ID}, datum_narozeni{datum_narozeni}, datum_vazeni{datum_vazeni}, tyden_vazeni{tyden_vazeni}, hmotnost{hmotnost}, datum_spek{datum_spek}, tyden_spek{tyden_spek}, spek{spek}, rije{rije}")
        return animal
    return None
