import decimal

from src.abstract_reader import AbstractReader
from src.book import Book


class Reader(AbstractReader):

    def __init__(self, first_name: str, last_name: str, reader_id: int):
        self._first_name = first_name
        self._last_name = last_name
        self._reader_id = reader_id
        self._borrowed_books = []
        self._reserved_books = []
        self._debt: decimal = 0

    def __str__(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def borrowed_books(self) -> list:
        return self._borrowed_books

    @property
    def debt(self) -> int:
        return self._debt

    @property
    def reserved_books(self) -> list:
        return self._reserved_books

    @property
    def reader_id(self) -> int:
        return self._reader_id

    def update(self, book) -> None:
        print(f"{book.title} is available in {book.available_copies} copies for {str(self)}.")

    def borrow_book(self, book: Book) -> None:
        self.borrowed_books.append(book)
        book.available_copies -= 1
        print(f"{str(book)} borrowed by {str(self)}.")

    def return_book(self, book: Book) -> None:
        self.borrowed_books.remove(book)
        book.available_copies += 1
        print(f"{str(book)} returned by {str(self)}.")

    def reserve_book(self, book: Book) -> None:
        self.reserved_books.append(book)
        print(f"{str(book)} reserved for {str(self)}.")