from src.book import Book


class Library:
    def __init__(self):
        self.books = [Book("Moby Dick"), Book("Alice in Wonderland"), Book("The Flight")]

    def display_books(self):
        for book in self.books:
            print(f"{book.title}, reserved: {book.reserved}, available: {book.available}")