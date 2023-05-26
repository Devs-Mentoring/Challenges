class Reader:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.books = []
        self.reserved_books = []
        self.debt = 0

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def display_books(self):
        for book in self.books:
            print(f"{book.title}")

    def display_reserved_books(self):
        for book in self.reserved_books:
            print(f"{book.title}")

    def update(self, book) -> None:
        print(f"{book.title} is available.")
