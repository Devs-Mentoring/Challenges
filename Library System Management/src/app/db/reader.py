from typing import List

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.selectable import Select
from src.app.schemas import Reader
from multipledispatch import dispatch

from src.app.db import engine


class ReaderDB:
    @staticmethod
    def reader(reader_id):
        with Session(engine) as session:
            return session.get(Reader, reader_id)

    @staticmethod
    @dispatch(str, str)
    def sel_login(first_name, surname) -> Select:
        stmt = select(Reader).where(and_(Reader.first_name == first_name, Reader.surname == surname))
        return stmt

    @staticmethod
    @dispatch(int)
    def sel_login(number) -> Select:
        stmt = select(Reader).where(Reader.number == number)
        return stmt

    @staticmethod
    def login(*args) -> Reader:
        with Session(engine) as session:
            try:
                stmt = ReaderDB.sel_login(*args)
            except NotImplementedError:
                return None
            reader = session.scalars(stmt).first()
            if reader:
                return reader.id
            return None

    @staticmethod
    def register(number, first_name, surname):
        with Session(engine) as session:
            reader = Reader(number=number, first_name=first_name, surname=surname)
            session.add_all([reader])
            try:
                session.commit()
            except IntegrityError:
                return None
            return reader.id

    @staticmethod
    @dispatch(int)
    def sel_readers(number) -> Select:
        return select(Reader).where(Reader.number == int(number))

    @staticmethod
    @dispatch(str, str)
    def sel_readers(first_name, surname) -> Select:
        return select(Reader).where(and_(Reader.first_name.like(first_name), Reader.surname.like(surname)))

    @staticmethod
    @dispatch(str)
    def sel_readers(name) -> Select:
        return select(Reader).where(or_(Reader.first_name.like(name), Reader.surname.like(name)))

    @staticmethod
    def find_readers(*args) -> List["Reader"]:
        with Session(engine) as session:
            stmt = ReaderDB.sel_readers(*args)
            readers = list(session.scalars(stmt).all())
            return readers

    @staticmethod
    def pay_fines(reader_id):
        with Session(engine) as session:
            reader = session.get(Reader, reader_id)
            reader.fines = 0.0
            session.commit()

    @staticmethod
    def get_fines(reader_id):
        with Session(engine) as session:
            reader = session.get(Reader, reader_id)
            return reader.fines
