from dataclasses import dataclass


@dataclass
class Library:
    books: list
    readers: list

    def find_book_by_title(self, title: str) -> None:
        for book in self.books:
            if book.title.lower() == title.lower():
                print(f"{str(book)} found.")
                return book
        print(f"{str(title)} not found.")
        return None

    def find_reader_by_id(self, reader_id: int) -> None:
        for reader in self.readers:
            if reader.reader_id == reader_id:
                print(f"Reader with id {reader_id}: {str(reader)} found.")
                return reader
        print(f"Reader with id {reader_id} not found.")
        return None

    def display_all_books(self) -> None:
        for book in self.books:
            print(f"{str(book)}, number of copies {str(book.available_copies)}")

    def display_all_readers(self) -> None:
        for reader in self.readers:
            print(f"{str(reader)}, id {str(reader.reader_id)}")
