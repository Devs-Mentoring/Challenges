from unittest.mock import Mock, call

from _pytest.fixtures import fixture

from src.abstract_reader import AbstractReader
from src.book import Book
from src.reader import Reader


class TestBook:

    @fixture
    def book(self) -> Book:
        return Book("The flight", "Exupery", "Publisher", 1990, 1)

    @fixture
    def reader(self) -> AbstractReader:
        return Reader("John", "Doe", 1)

    @fixture
    def book(self) -> Book:
        return Book("The flight", "Exupery", "Publisher", 1990, 3)

    def test_add_subscriber(self, book: Book, reader: AbstractReader):
        book.add_subscriber(reader)
        assert len(book._subscribers) == 1

    def test_unsubscribe(self, book: Book, reader: AbstractReader):
        book.add_subscriber(reader)
        book.unsubscribe(reader)
        assert len(book._subscribers) == 0

    def test_notify_subscribers(self, book: Book, reader: AbstractReader):
        mock = Mock(book.notify_subscribers(), return_value=None)
        mock(1)
        calls = [call(1)]
        mock.assert_has_calls(calls)
