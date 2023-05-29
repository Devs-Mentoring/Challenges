from datetime import datetime, timedelta


class Book:
    book_instances = {}
    book_id_counter = 0


    def __new__(cls, title, author, publisher, year, inventory):
        book_key = (title, author, publisher, year)
        if book_key not in cls.book_instances:
            instance = super().__new__(cls)
            cls.book_instances[book_key] = instance
            return instance
        return cls.book_instances[book_key]

    def __init__(self, title, author, publisher, year, inventory):
        if not hasattr(self, "title"):
            self.book_id = Book.book_id_counter
            self.title = title
            self.author = author
            self.publisher = publisher
            self.year = year
            self.inventory = inventory
            self.reservations = []

            print(f"Successfully created book. {self}")
            Book.book_id_counter += 1
        else:
            print("Book already exists, returned instance.")

    def __repr__(self):
        return f"ID: {self.book_id}, Title: {self.title}, Year: {self.year}"


class Reader:
    reader_instances = {}
    reader_id_counter = 0

    def __new__(cls, name, surname):
        reader_key = (name, surname)
        if reader_key not in cls.reader_instances:
            instance = super().__new__(cls)
            cls.reader_instances[reader_key] = instance
        return cls.reader_instances[reader_key]

    def __init__(self, name, surname):
        if not hasattr(self, "reader_id"):
            self.reader_id = Reader.reader_id_counter
            self.name = name
            self.surname = surname
            self.borrowed_books = {}
            self.history = []
            Reader.reader_id_counter += 1
            print(f"Successfully created reader {self}")
        else:
            print("Reader already exists, returned instance.")

    def __repr__(self):
        return f"ID: {self.reader_id}, Name: {self.name}, Surname: {self.surname}"

class BookManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.books = {}

    def add_book(self, title, author, publisher, year, inventory):
        new_book = Book(title, author, publisher, year, inventory)
        self.books[new_book.book_id] = new_book

    def get_book(self, book_id):
        try:
            book = self.books[book_id]
            return self.books[book_id]
        except KeyError:
            print(f"Book with ID: {book_id} doesnt exist")

class ReaderManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.readers = {}

    def add_reader(self, name, surname):
        new_reader = Reader(name, surname)
        self.readers[new_reader.reader_id] = new_reader

    def get_reader(self, reader_id):
        try:
            reader = self.readers[reader_id]
            return self.readers[reader_id]
        except KeyError:
            print(f"Reader with ID: {reader_id} doesnt exist")


class Library:
    def __init__(self):
        self.book_manager = BookManager()
        self.reader_manager = ReaderManager()

    def add_book(self, title, author, publisher, year, inventory):
        self.book_manager.add_book(title, author, publisher, year, inventory)

    def add_reader(self, name, surname):
        self.reader_manager.add_reader(name, surname)


    def notify_reader_book_avaliable(self, book, reader):
        print(f"The book {book.title} is now avaliable")

    def notify_reader_book_overdue(self, book, reader):
        delay = datetime.now() - reader.borrowed_books[book]
        print(f"The book {book.title} is overdue by {delay} return it asap")


    def borrow_book(self, book_id, reader_id):
        book = self.book_manager.get_book(book_id)
        reader = self.reader_manager.get_reader(reader_id)
        try:
            reader.borrowed_books[book]
            print("Reader already borrowed this book")

        except KeyError:
            if book and reader:
                if book.inventory > 0:
                    book.inventory -= 1
                    reader.borrowed_books[book] = datetime.now() + timedelta(days=30)
                    reader.history.append((book, datetime.now(), "Borrowed"))
                elif book.inventory == 0:
                    book.reservations.append(reader)
                    print(
                        f"Book is not avaliable at the moment but reservation has been made"
                    )

    def return_book(self, book_id, reader_id):
        book = self.book_manager.get_book(book_id)
        reader = self.reader_manager.get_reader(reader_id)

        if book and reader:
            if book in reader.borrowed_books:
                reader.borrowed_books.pop(book)
                reader.history.append((book, datetime.now(), "Returned"))
                book.inventory += 1
                if book.reservations:
                    next_reader = book.reservations.pop(0)
                    self.borrow_book(book.book_id, next_reader.reader_id)
                    self.notify_reader_book_avaliable(book, next_reader)
        else:
            print("Book or reader does not exist")


if __name__ == "__main__":
    pass
