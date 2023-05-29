from datetime import date, timedelta

from src.event_handler import EventHandler
from src.library import Library
from src.menu import get_title
from src.reader import Reader


class ReaderManager:
    def __init__(self, reader: Reader, event_handler: EventHandler, library: Library):
        self.reader = reader
        self.event_handler = event_handler
        self.library = library

    def borrow_book(self):
        title = get_title()
        for book in self.library.books:
            if book in self.reader.reserved_books:
                return self._borrow_reserved_book(book)
            elif book.title == title and book.reserved is False and book.available is True:
                return self._borrow_available_book(book)

    def _borrow_available_book(self, book):
        book.available = False
        self.reader.books.append(book)
        self.event_handler.update_history(self.reader, book, date.today(), date.today() + timedelta(days=14))
        return book

    def _borrow_reserved_book(self, book):
        book.available = False
        book.reserved = False
        self.reader.reserved_books.remove(book)
        self.reader.books.append(book)
        self.event_handler.update_history(self.reader, book, date.today(), date.today() + timedelta(days=14))
        return book

    def reserve_book(self):
        title = get_title()
        for book in self.library.books:
            if book.title == title:
                book.reserved = True
                self.reader.reserved_books.append(book)
                return book

    def resign_from_reservation(self):
        title = get_title()
        for book in self.reader.reserved_books:
            if book.title == title:
                self.reader.reserved_books.remove(book)
                book.reserved = False

    def return_book(self):
        title = get_title()
        for book in self.reader.books:
            if book.title == title:
                self.reader.books.remove(book)
                book.available = True
                self.event_handler.update_history(self.reader, book,
                                                  self.event_handler.get_borrow_date(self.reader, book), date.today())
                self.event_handler.apply_penalty_for_the_reader(book, self.reader, date.today())
                return book
