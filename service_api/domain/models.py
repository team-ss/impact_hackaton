from typing import List

from sqlalchemy import MetaData, Table, Column, Integer, Text, Float

metadata = MetaData()

CarPollution = Table(
    "car_pollution",
    metadata,
    Column("Manufacturer", Text, nullable=True),
    Column("Model", Text, nullable=True),
    Column("Description", Text, nullable=True),
    Column("Transmission", Text, nullable=True),
    Column("Engine Capacity", Integer, nullable=True),
    Column("Fuel Type", Text, nullable=True),
    Column("Metric Urban (Cold)", Float, nullable=True),
    Column("Metric Extra-Urban", Float, nullable=True),
    Column("Metric Combined", Float, nullable=True),
    Column("Imperial Urban (Cold)", Float, nullable=True),
    Column("Imperial Extra-Urban", Float, nullable=True),
    Column("Imperial Combined", Float, nullable=True),
    Column("CO2 g/km", Integer),
    Column("Fuel Cost 12000 Miles", Text, nullable=True),
    Column("Total cost / 12000 miles", Text, nullable=True),
    Column("Euro Standard", Integer, nullable=True),
    Column("Noise Level dB(A)", Integer, nullable=True),
    Column("Emissions CO [mg/km]", Integer, nullable=True),
    Column("Emissions NOx [mg/km]", Integer, nullable=True),
    Column("THC + NOx Emissions [mg/km]", Integer, nullable=True),
    Column("Particulates [No.] [mg/km]", Float, nullable=True),
)

models: List[Table] = [CarPollution, ]
