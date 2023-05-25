from typing import List
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.selectable import Select
from src.app.schemas import Book, Rent, Reservation
from multipledispatch import dispatch

from src.app.db import engine
from src.app.db.rent import RentDB
from src.app.db.reservation import ReservationDB

class BookDB:
    @staticmethod
    def add(**kwargs):
        with Session(engine) as session:
            book = Book(**kwargs)
            session.add_all([book])
            try:
                session.commit()
            except IntegrityError:
                return None
            return book.id

    @staticmethod
    def update():
        pass

    @staticmethod
    def get(book_id):
        with Session(engine) as session:
            return session.get(Book, book_id)

    @staticmethod
    def remove(book_id):
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book:
                print("Book not found")
                return
            yes = input("Book found, are you ? (Y/N)")
            if yes != "Y":
                return
            session.delete(book)
            session.commit()
            print("deleted")

    @staticmethod
    @dispatch(str, str)
    def sel_books(title, author) -> Select:
        return select(Book).where(and_(Book.title.like(f"%{title}%"), Book.author.like(f"%{author}%")))

    @staticmethod
    @dispatch(str)
    def sel_books(phrase) -> Select:
        return select(Book).where(or_(Book.title.like(f"%{phrase}%"), Book.author.like(f"%{phrase}%")))

    @staticmethod
    def find_books(*args) -> (List["Book"], List[str]):
        with Session(engine) as session:
            stmt = BookDB.sel_books(*args)
            books = list(session.scalars(stmt).all())
            books_display = []
            for book in books:
                remaining = book.available - len(book.rents)
                reservations = len(book.reservations)
                books_display.append(f"[{book.id}] | {book.title}, {book.author} | {book.year} "
                                     f"| ({remaining}/{book.available}) "
                                     f"| R({reservations})")
            return books, books_display
