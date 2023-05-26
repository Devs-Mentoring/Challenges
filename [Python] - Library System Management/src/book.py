from src.reader import Reader


class Book:
    def __init__(self, title):
        self.title = title
        self.reserved = False
        self.subscribers = []
        self.available = True

    def add_subscriber(self, reader: Reader) -> None:
        self.subscribers.append(reader)

