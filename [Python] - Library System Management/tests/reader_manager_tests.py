import unittest
from unittest.mock import MagicMock, patch

from src.event_handler import EventHandler
from src.library import Library
from src.reader import Reader
from src.reader_manager import ReaderManager


class ReaderManagerTests(unittest.TestCase):
    def setUp(self):
        self.reader = Reader("John", "password")
        self.event_handler = EventHandler()
        self.library = Library()
        self.manager = ReaderManager(self.reader, self.event_handler, self.library)

    @patch('builtins.input', return_value='Book 1')
    def test_borrow_book_with_available_book(self, mock_input):
        book = MagicMock()
        book.title = "Book 1"
        book.reserved = False
        book.available = True
        self.library.books.append(book)

        borrowed_book = self.manager.borrow_book()

        self.assertEqual(len(self.reader.books), 1)
        self.assertEqual(borrowed_book, book)
        self.assertFalse(book.available)
        mock_input.assert_called_once_with("Title: ")

    @patch('builtins.input', return_value='Book 2')
    def test_borrow_book_with_reserved_book(self, mock_input):
        book = MagicMock()
        book.title = "Book 2"
        book.reserved = True
        book.available = False
        self.library.books.append(book)
        self.reader.reserved_books.append(book)

        borrowed_book = self.manager.borrow_book()

        self.assertEqual(len(self.reader.books), 1)
        self.assertEqual(borrowed_book, book)
        self.assertFalse(book.available)
        self.assertFalse(book.reserved)
        self.assertNotIn(book, self.reader.reserved_books)
        mock_input.assert_called_once_with("Title: ")

    @patch('builtins.input', return_value='Book 3')
    def test_reserve_book(self, mock_input):
        book = MagicMock()
        book.title = "Book 3"
        book.reserved = False
        self.library.books.append(book)

        reserved_book = self.manager.reserve_book()

        self.assertTrue(book.reserved)
        self.assertEqual(reserved_book, book)
        self.assertIn(book, self.reader.reserved_books)
        mock_input.assert_called_once_with("Title: ")

    @patch('builtins.input', return_value='Book 4')
    def test_resign_from_reservation(self, mock_input):
        book = MagicMock()
        book.title = "Book 4"
        book.reserved = True
        self.reader.reserved_books.append(book)

        self.manager.resign_from_reservation()

        self.assertFalse(book.reserved)
        self.assertNotIn(book, self.reader.reserved_books)
        mock_input.assert_called_once_with("Title: ")

    @patch('builtins.input', return_value='Book 5')
    def test_return_book(self, mock_input):
        book = MagicMock()
        book.title = "Book 5"
        book.available = False
        self.reader.books.append(book)

        returned_book = self.manager.return_book()

        self.assertTrue(book.available)
        self.assertNotIn(book, self.reader.books)
        self.assertEqual(returned_book, book)
        mock_input.assert_called_once_with("Title: ")

