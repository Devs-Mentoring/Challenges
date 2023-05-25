import datetime
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.app.schemas import Rent, Book, Reservation
from src.app.db import engine


class ReservationDB:

    @staticmethod
    def reserved_by_reader(reader_id, book_id):
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book:
                return None
            stmt = select(Reservation).where(and_(Reservation.book_id == book_id, Reservation.reader_id == reader_id))
            return bool(session.scalars(stmt).first())

    @staticmethod
    def check_if_reserved(reader_id, book_id):
        """return: True - if book reserved, False - if book available """
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book:
                return None
            reserved_by_reader = ReservationDB.reserved_by_reader(reader_id, book_id)
            if reserved_by_reader:
                return False
            stmt = select(Rent).where(Rent.book_id == book_id)
            rented = len(list(session.scalars(stmt).all()))
            stmt = select(Reservation).where(Reservation.book_id == book_id)
            reserved = len(list(session.scalars(stmt).all()))
            return (book.available - rented - reserved) <= 0

    @staticmethod
    def reserve(reader_id, book_id):
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book or ReservationDB.reserved_by_reader(reader_id, book_id):
                return None
            reservation = Reservation(reader_id=reader_id, book_id=book_id)
            session.add_all([reservation])
            try:
                session.commit()
            except IntegrityError:
                return None
            return reservation.id

    @staticmethod
    def end_reservation_by_rent(session, reader_id, book_id):
        stmt = select(Reservation).where(and_(Reservation.book_id == book_id, Reservation.reader_id == reader_id))
        reservation = session.scalars(stmt).first()
        if reservation:
            session.delete(reservation)

    @staticmethod
    def end_reservation(reservation_id):
        with Session(engine) as session:
            reservation = session.get(Rent, reservation_id)
            if not reservation:
                return False
            session.delete(reservation)
            session.commit()
            return True

    @staticmethod
    def reader_reservations(reader_id):
        with Session(engine) as session:
            stmt = select(Reservation).where(Reservation.reader_id == reader_id)
            reservations = list(session.scalars(stmt).all())
            reservations_display = [reservation.book.title for reservation in reservations]
            return reservations, reservations_display
