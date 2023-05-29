import unittest
from io import StringIO
from unittest.mock import patch

from src.library import Library


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()

    def test_display_books(self):
        expected_output = "Moby Dick, reserved: False, available: True\n" \
                         "Alice in Wonderland, reserved: False, available: True\n" \
                         "The Flight, reserved: False, available: True\n"

        # Capture printed output
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.library.display_books()

            printed_output = mock_stdout.getvalue()

            self.assertEqual(printed_output, expected_output)
