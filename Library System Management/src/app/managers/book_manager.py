from src.app.db.book import BookDB


class BookManager:
    COMMANDS = {"always": ["add_book", "remove_book", "update_book", "find_books"]}

    @staticmethod
    def add_book():
        title = input("title: ")
        author = input("author: ")
        publisher = input("publisher: ")
        year = int(input("year: "))
        available = int(input("available: "))
        book = BookDB.add(title=title, author=author, publisher=publisher, year=year, available=available)
        print("created!")
        return book

    @staticmethod
    def update_book():
        pass

    @staticmethod
    def remove_book():
        book_id = int(input("Book id: "))
        book = BookDB.get(book_id)
        if not book:
            print("Book not found")
            return
        yes = input("Book found, are you ? (Y/N)")
        if yes != "Y":
            return
        BookDB.remove(book_id)
        print("deleted!")

    @staticmethod
    def find_books():
        book_data = input("<Title> | <Author> | <Title>,<Author>: ")
        args = book_data.split(", ")
        books, books_display = BookDB.find_books(*args)
        for book in books_display:
            print(book)
