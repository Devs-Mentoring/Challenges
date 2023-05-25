import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


currentdir = os.getcwd()
engine = create_engine(f"sqlite:///{currentdir}\\instance\\test.db", echo=False)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(engine)



