from datetime import date

from src.event_handler import EventHandler
from src.library import Library
from src.menu import get_password, get_choice, get_username, display_menu, display_user_menu
from src.reader import Reader
from src.reader_manager import ReaderManager


class App:
    def __init__(self):
        self.library = Library()
        self.event_handler = EventHandler()
        self.users = []
        self.options = {1: self._login, 2: self._register_user, 3: self.event_handler.display_history,
                        4: self.finish}

    def run(self):
        while True:
            try:
                choice = int(get_choice(display_menu()))
            except ValueError:
                self.show_error()
            else:
                self.options.get(choice, self.show_error)()

    def _register_user(self):
        username = get_username()
        password = get_password()
        reader = Reader(username, password)
        if reader in self.users:
            print("Reader already exists. Please choose a different username.")
            return
        self.users.append(reader)
        print("Registration successful!")

    def _login(self):
        username = get_username()
        password = get_password()
        user = self._get_user_by_name_and_password(username, password)
        reader_manager = ReaderManager(user, self.event_handler, self.library)
        self._run_user_submenu(reader_manager, user)

    def _run_user_submenu(self, reader_manager, user):
        try:
            if user in self.users:
                print("Login successful!")
                self._execute_user_submenu(reader_manager)
            else:
                print("Wrong login or password.")
        except AttributeError:
            print("Wrong login or password.")

    def _get_user_by_name_and_password(self, name, password):
        for user in self.users:
            if user.name == name and user.password == password:
                return user

    def _execute_user_submenu(self, reader_manager: ReaderManager):
        while True:
            self.event_handler.remind(reader_manager.reader, date.today())
            self.event_handler.notify_subscribers(self.library, reader_manager.reader)
            options = {1: self.finish, 2: self.library.display_books, 3: reader_manager.borrow_book,
                       4: reader_manager.reader.display_books,
                       5: reader_manager.return_book,
                       6: reader_manager.reserve_book, 7: reader_manager.reader.display_reserved_books,
                       8: reader_manager.resign_from_reservation}
            try:
                choice = int(get_choice(display_user_menu()))
            except ValueError:
                self.show_error()
            else:
                options.get(choice, self.show_error)()

    @staticmethod
    def finish():
        print("Program finished.")
        exit()

    @staticmethod
    def show_error():
        print("Error!")
