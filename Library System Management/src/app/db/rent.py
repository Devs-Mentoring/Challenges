import datetime
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.app.schemas import Rent, Book, Reservation, Historical, Notification, Reader
from src.app.db import engine
from src.app.db.reservation import ReservationDB
from src.app.settings import DAY_FINE, REMIND_BEFORE


class RentDB:

    @staticmethod
    def check_availability(book_id):
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book:
                return None
            stmt = select(Rent).where(and_(Rent.book_id == book_id))
            rented = len(list(session.scalars(stmt).all()))
            return book.available - rented


    @staticmethod
    def check_if_rented(reader_id, book_id):
        with Session(engine) as session:
            stmt = select(Rent).where(and_(Rent.book_id == book_id, Rent.reader_id == reader_id))
            rented = session.scalars(stmt).first()
            return bool(rented)

    @staticmethod
    def rent(reader_id, book_id):
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book or RentDB.check_if_rented(reader_id, book_id) \
                    or ReservationDB.check_if_reserved(reader_id, book_id):
                return None
            rent = Rent(reader_id=reader_id, book_id=book_id)
            session.add_all([rent])
            ReservationDB.end_reservation_by_rent(session, reader_id, book_id)
            try:
                session.commit()
            except IntegrityError:
                return None
            return rent.id

    @staticmethod
    def return_book(rent_id):
        with Session(engine) as session:
            rent = session.get(Rent, rent_id)
            if not rent:
                return False
            historical = Historical(reader_id=rent.reader_id, book_id=rent.book_id, start=rent.start,
                                    end=datetime.datetime.utcnow())
            session.add_all([historical])
            session.delete(rent)
            session.commit()
            return True

    @staticmethod
    def get_active_rents(reader_id):
        with Session(engine) as session:
            stmt = select(Rent).where(Rent.reader_id == reader_id)
            rents = list(session.scalars(stmt).all())
            rents_display = [rent.book.title for rent in rents if rent.book]
            return rents, rents_display

    @staticmethod
    def get_historical_rents(reader_id):
        with Session(engine) as session:
            stmt = select(Historical).where(Historical.reader_id == reader_id)
            rents = list(session.scalars(stmt).all())
            rents_display = [f"{rent.start.strftime('%d/%m/%Y %H:%M')} - {rent.end.strftime('%d/%m/%Y %H:%M')}: " \
                             f"{rent.book.title}" for rent in rents]
            return rents, rents_display

    @staticmethod
    def create_notifications_for_reservations(book_id):
        with Session(engine) as session:
            book = session.get(Book, book_id)
            stmt = select(Reservation).where(Reservation.book_id == book_id)
            reservations = list(session.scalars(stmt).all())
            message = f"Book: {book.title} is now available"
            notifications = []
            for reservation in reservations:
                notifications.append(Notification(reader_id=reservation.reader_id, message=message))
            session.add_all(notifications)
            session.commit()

    @staticmethod
    def calc_fine(rent):
        expected_return = rent.start + datetime.timedelta(days=rent.max_days)
        if datetime.datetime.utcnow() <= expected_return:
            return 0.0
        time_after = datetime.datetime.utcnow() - expected_return
        return time_after.days * DAY_FINE

    @staticmethod
    def calc_remaining_days(rent):
        expected_return = rent.start + datetime.timedelta(days=rent.max_days)
        time_left = expected_return - datetime.datetime.utcnow()
        return time_left.days

    @staticmethod
    def check_for_delays(reader_id):
        reminders = []
        with Session(engine) as session:
            stmt = select(Rent).where(Rent.reader_id == reader_id)
            rents = list(session.scalars(stmt).all())

            for rent in rents:
                remain = RentDB.calc_remaining_days(rent)
                if 0 < remain < REMIND_BEFORE:
                    reminders.append(f"You have {remain} days left to return {rent.book.title}")
                elif remain <= 0:
                    reminders.append(f"Returning of {rent.book.title} is delayed for {-1*remain} days")
        return reminders

    @staticmethod
    def charge_fine(reader_id, fine):
        with Session(engine) as session:
            reader = session.get(Reader, reader_id)
            reader.fines += fine
            session.commit()

    @staticmethod
    def create_fine_notification(reader_id, fine):
        with Session(engine) as session:
            message = f"You were charged {fine} PLN for late return"
            notification = Notification(reader_id=reader_id, message=message)
            session.add_all([notification])
            session.commit()
