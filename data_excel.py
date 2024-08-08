import pandas as pd
from db import db
from sqlalchemy import create_engine



class GrowthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    growth_rate = db.Column(db.Float, nullable=True)


def calculate_growth_curve():
    growth_data = GrowthData.query.all()
    df = pd.DataFrame([(d.age, d.weight) for d in growth_data], columns=['age', 'weight'])
    df['growth_rate'] = df['weight'] / df['age']

    for index, row in df.iterrows():
        growth_data[index].growth_rate = row['growth_rate']

    db.session.commit()
    return df


if __name__ == "__main__":
    engine = create_engine('sqlite:///instance/database_gilts.db')
    df = pd.read_sql('animals', engine)
    print(df)