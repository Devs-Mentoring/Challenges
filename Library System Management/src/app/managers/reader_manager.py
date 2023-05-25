from src.app.db.reader import ReaderDB


class ReaderManager:
    COMMANDS = {"logged": ["logout", "pay_fines"], "unlogged": ["login", "register", "find_readers"]}

    def __init__(self):
        self._reader = None

    @property
    def reader(self):
        return ReaderDB.reader(self._reader)

    def login(self):
        login_data = input("<Number> | <First name> <Surname>: ")
        if login_data.isnumeric():
            args = [int(login_data)]
        else:
            args = login_data.split(' ')
        reader_id = ReaderDB.login(*args)
        if reader_id:
            self._reader = reader_id
            print("Logged in")
        else:
            print("Login error")

    def logout(self) -> None:
        self._reader = None

    def register(self):
        number = input("reader number: ")
        first_name = input("first name: ")
        surname = input("surname: ")
        reader_id = ReaderDB.register(number, first_name, surname)
        if reader_id:
            self._reader = reader_id
            print("Registered and logged in")
        else:
            print("Registration error")

    @staticmethod
    def find_readers():
        reader_data = input("<Number> | <First name> | <Surname>: ")
        if reader_data.isnumeric():
            args = [int(reader_data)]
        else:
            args = reader_data.split(" ")
        readers = ReaderDB.find_readers(*args)
        for reader in readers:
            print(reader)

    def pay_fines(self):
        if not self._reader:
            return
        ReaderDB.pay_fines(self._reader)
