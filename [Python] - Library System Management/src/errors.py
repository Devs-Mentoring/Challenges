from src.abstract_reader import AbstractReader
from src.book import Book
from src.library import Library


class Errors:
    def __init__(self, library: Library):
        self._library = library

    def borrow_book(self, reader: AbstractReader, book: Book) -> None:
        if book not in self._library.books:
            raise ValueError("Book not added to library.")
        if book.available_copies == 0:
            raise ValueError("Book is currently unavailable.")
        if book in reader.borrowed_books:
            raise ValueError("You have already borrowed this book.")
        if reader is None:
            raise ValueError("Reader undefined")

    def return_book(self, reader: AbstractReader, book: Book) -> None:
        if book not in self._library.books:
            raise ValueError("Book is not from this library.")
        if book not in reader.borrowed_books:
            raise ValueError("You did not borrowed this book.")

    def reserve_book(self, reader: AbstractReader, book: Book) -> None:
        if book not in self._library.books:
            raise ValueError("Book was not added to library.")
        if book in reader.reserved_books:
            raise ValueError("You have already reserved this book.")
        if book.available_copies >= 1 and book not in reader.borrowed_books:
            raise ValueError("You do not need to subscribe. Book is available")
        if book in reader.borrowed_books:
            raise ValueError("You borrowed this book.")

    def add_book(self, the_book: Book, book: Book) -> None:
        if str(the_book) == str(book):
            raise ValueError("Book already exists in the library.")

    def add_reader(self, the_reader: AbstractReader, reader: AbstractReader) -> None:
        if the_reader.reader_id == reader.reader_id:
            raise ValueError("Reader already exists in the library.")
