import datetime
from sqlalchemy import select, update, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.app.schemas import Notification
from src.app.db import engine


class NotificationDB:

    @staticmethod
    def add(reader_id, message):
        with Session(engine) as session:
            notification = Notification(reader_id=reader_id, message=message)
            session.add_all([notification])
            try:
                session.commit()
            except IntegrityError:
                return None
            return notification.id

    @staticmethod
    def all_read(reader_id):
        with Session(engine) as session:
            stmt = update(Notification).where(Notification.reader_id == reader_id).values(read=True)
            session.execute(stmt)
            session.commit()

    @staticmethod
    def new(reader_id):
        with Session(engine) as session:
            stmt = select(Notification).where(and_(Notification.reader_id == reader_id, Notification.read.is_(False)))
            notifications = list(session.scalars(stmt).all())
            notifications_display = [notify.message for notify in notifications]
            return notifications, notifications_display

    @staticmethod
    def all(reader_id):
        with Session(engine) as session:
            stmt = select(Notification).where(Notification.reader_id == reader_id)
            notifications = list(session.scalars(stmt).all())
            notifications_display = [notify.message for notify in notifications]
            return notifications, notifications_display
