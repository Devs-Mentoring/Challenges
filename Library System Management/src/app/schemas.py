import datetime

from typing import List

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import func

from src.app.db import Base


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    author: Mapped[str] = mapped_column(String(30))
    publisher: Mapped[str] = mapped_column(String(30), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    available: Mapped[int] = mapped_column(Integer, default=1)
    rents: Mapped[List["Rent"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    historical: Mapped[List["Historical"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("title", "author", name='same_book'),)

    def __repr__(self) -> str:
        return f"{self.id} | {self.title}, {self.author} | {self.year} | ({self.available})"


class Reader(Base):
    __tablename__ = "reader"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer, unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    fines: Mapped[float] = mapped_column(Float, default=0.0)
    rents: Mapped[List["Rent"]] = relationship(back_populates="reader", cascade="all, delete-orphan")
    historical: Mapped[List["Historical"]] = relationship(back_populates="reader", cascade="all, delete-orphan")
    reserved_books: Mapped[List["Reservation"]] = relationship(back_populates="reader", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="reader", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.number}, {self.first_name} {self.surname}"


class Rent(Base):
    __tablename__ = "rent"
    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("reader.id"))
    reader: Mapped["Reader"] = relationship(back_populates="rents")
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped["Book"] = relationship(back_populates="rents")
    start: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(()))
    max_days: Mapped[int] = mapped_column(Integer, default=30)

    def __repr__(self) -> str:
        return f"reader:{self.reader_id} book:{self.book_id} | {self.start}"


class Historical(Base):
    __tablename__ = "historical"
    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("reader.id"))
    reader: Mapped["Reader"] = relationship(back_populates="historical")
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped["Book"] = relationship(back_populates="historical")
    start: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(()))
    end: Mapped[datetime.datetime] = mapped_column(DateTime, default=None, nullable=True)

    def __repr__(self) -> str:
        return f"reader:{self.reader_id} book:{self.book_id} | {self.start} - {self.end}"


class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("reader.id"))
    reader: Mapped["Reader"] = relationship(back_populates="reserved_books")
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped["Book"] = relationship(back_populates="reservations")
    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(()))

    def __repr__(self) -> str:
        return f"reserved: reader:{self.reader_id} book:{self.book_id} | {self.created}"


class Notification(Base):
    __tablename__ = "notification"
    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("reader.id"))
    reader: Mapped["Reader"] = relationship(back_populates="notifications")
    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(()))
    message: Mapped[str] = mapped_column(String(250))
    read: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.created}: {self.message}"
