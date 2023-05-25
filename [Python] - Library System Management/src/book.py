from src.abstract_reader import AbstractReader


class Book:

    def __init__(self, title: str, author: str, publisher: str, year: int, num_copies: int):
        self._title = title
        self._author = author
        self._publisher = publisher
        self._year = year
        self._num_copies = num_copies
        self._available_copies = num_copies
        self._subscribers: list['AbstractReader'] = []

    def __str__(self) -> str:
        return self.title

    @property
    def title(self) -> str:
        return self._title

    @property
    def available_copies(self) -> int:
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value) -> None:
        self._available_copies = value

    def add_subscriber(self, reader: AbstractReader) -> None:
        print(f"{str(reader)} subscribed for {str(self)}.")
        self._subscribers.append(reader)

    def unsubscribe(self, reader: AbstractReader) -> None:
        print(f"{str(reader)} unsubscribed from {str(self)}.")
        if reader in self._subscribers:
            self._subscribers.remove(reader)

    def notify_subscribers(self) -> None:
        if self.available_copies == 1 and len(self._subscribers) > 0:
            print("Notifying all subscribers.")
            for reader in self._subscribers:
                reader.update(self)
