import sys
from datetime import date

from src.event_handler import EventHandler
from src.library import Library
from src.menu import Menu
from src.reader import Reader
from src.reader_manager import ReaderManager


class App:
    def __init__(self):
        self.users = []
        self.menu = Menu()

    def run(self):
        event_handler = EventHandler()
        library = Library()
        while True:
            self.menu.display_menu()
            choice = input("Choose: ")
            if choice == "1":
                self._login(library, event_handler)
            elif choice == "2":
                self._register_user()
            elif choice == "3":
                event_handler.display_history()
            elif choice == "4":
                sys.exit()
            else:
                print("Invalid choice.")

    def _register_user(self):
        username = self.menu.get_username()
        password = self.menu.get_password()
        reader = Reader(username, password)
        if reader in self.users:
            print("Reader already exists. Please choose a different username.")
            return
        self.users.append(reader)
        print("Registration successful!")

    def _login(self, library, event_handler):
        username = self.menu.get_username()
        password = self.menu.get_password()
        reader = self._get_user_by_name_and_password(username, password)
        reader_manager = ReaderManager(reader, event_handler, library)
        try:
            if reader in self.users:
                print("Login successful!")
                self._run_user_submenu(library, reader_manager, event_handler)
            else:
                print("Wrong login or password. else")
        except AttributeError:
            print("Wrong login or password. attr error")

    def _get_user_by_name_and_password(self, name, password):
        for user in self.users:
            if user.name == name and user.password == password:
                return user

    def _run_user_submenu(self, library: Library, reader_manager: ReaderManager, event_handler: EventHandler):
        while True:
            event_handler.remind(reader_manager.reader, date.today())
            event_handler.notify_subscribers(library, reader_manager.reader)
            self.menu.display_user_menu()
            choice = input("Choose: ")
            if choice == "1":
                return
            elif choice == "2":
                library.display_books()
            elif choice == "3":
                reader_manager.borrow_book()
            elif choice == "4":
                reader_manager.reader.display_books()
            elif choice == "5":
                reader_manager.return_book()
            elif choice == "6":
                reader_manager.reserve_book()
            elif choice == "7":
                reader_manager.reader.display_reserved_books()
            else:
                print("Invalid input")
