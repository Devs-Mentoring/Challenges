import unittest
from unittest.mock import MagicMock

from src.reader import Reader


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.reader = Reader("John Doe", "password")

    def test_init(self):
        self.assertEqual(self.reader.name, "John Doe")
        self.assertEqual(self.reader.password, "password")
        self.assertEqual(self.reader.books, [])
        self.assertEqual(self.reader.reserved_books, [])
        self.assertEqual(self.reader.debt, 0)

    def test_eq(self):
        reader1 = Reader("John Doe", "password")
        reader3 = Reader("Jane Smith", "password")

        self.assertEqual(self.reader, reader1)
        self.assertNotEqual(self.reader, reader3)

    def test_display_books(self):
        book1 = MagicMock()
        book1.title = "Book 1"
        book2 = MagicMock()
        book2.title = "Book 2"

        self.reader.books = [book1, book2]

        with unittest.mock.patch("builtins.print") as mock_print:
            self.reader.display_books()
            expected_output = [unittest.mock.call("Book 1"), unittest.mock.call("Book 2")]
            mock_print.assert_has_calls(expected_output)

    def test_display_reserved_books(self):
        book1 = MagicMock()
        book1.title = "Book 1"
        book2 = MagicMock()
        book2.title = "Book 2"

        self.reader.reserved_books = [book1, book2]

        with unittest.mock.patch("builtins.print") as mock_print:
            self.reader.display_reserved_books()
            expected_output = [unittest.mock.call("Book 1"), unittest.mock.call("Book 2")]
            mock_print.assert_has_calls(expected_output)

    def test_update(self):
        book = MagicMock()
        book.title = "Book 1"

        with unittest.mock.patch("builtins.print") as mock_print:
            self.reader.update(book)
            mock_print.assert_called_once_with("Book 1 is available.")
