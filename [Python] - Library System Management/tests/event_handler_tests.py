import unittest
from datetime import date
from unittest.mock import MagicMock, patch
from src.book import Book
from src.library import Library
from src.reader import Reader
from src.event_handler import EventHandler


class EventHandlerTests(unittest.TestCase):
    def setUp(self):
        self.event_handler = EventHandler()
        self.reader = Reader("John", "password")
        self.book = Book("Moby Dick")
        self.library = Library()

    def test_update_history(self):
        borrow_date = date(2021, 1, 1)
        return_date = date(2021, 1, 15)
        self.event_handler.update_history(self.reader, self.book, borrow_date, return_date)

        self.assertEqual(len(self.event_handler._list_of_events), 1)
        event = self.event_handler._list_of_events[0]
        self.assertEqual(event.reader_name, self.reader.name)
        self.assertEqual(event.book_title, self.book.title)
        self.assertEqual(event.borrow_date, borrow_date)
        self.assertEqual(event.return_date, return_date)

    def test_apply_penalty_for_the_reader(self):
        borrow_date = date(2021, 1, 1)
        return_date = date(2021, 1, 15)
        self.event_handler.update_history(self.reader, self.book, borrow_date, return_date)

        today = date(2021, 1, 20)
        self.event_handler.apply_penalty_for_the_reader(self.book, self.reader, today)
        self.assertEqual(self.reader.debt, 25)

    @patch("builtins.print")
    def test_remind(self, mock_print):
        borrow_date = date(2021, 1, 2)
        return_date = date(2021, 1, 15)
        self.reader.books.append(self.book)
        self.event_handler.update_history(self.reader, self.book, borrow_date, return_date)

        today = date(2021, 1, 10)
        self.event_handler.remind(self.reader, today)
        mock_print.assert_called_with(f"You have 5 days, 0:00:00 to return {self.book.title}.")

    def test_notify_subscribers(self):
        self.book.available = True
        self.library.books.append(self.book)
        self.reader.reserved_books.append(self.book)

        self.reader.update = MagicMock()
        self.event_handler.notify_subscribers(self.library, self.reader)

        self.reader.update.assert_called_once()
