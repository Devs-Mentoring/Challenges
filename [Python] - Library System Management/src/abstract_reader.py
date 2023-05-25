from abc import abstractmethod, ABC


class AbstractReader(ABC):

    @property
    @abstractmethod
    def borrowed_books(self):
        pass

    @property
    @abstractmethod
    def debt(self):
        pass

    @property
    @abstractmethod
    def reserved_books(self):
        pass

    @property
    @abstractmethod
    def reader_id(self):
        pass

    @abstractmethod
    def update(self, book) -> None:
        pass

    @abstractmethod
    def borrow_book(self, book) -> None:
        pass

    @abstractmethod
    def return_book(self, book) -> None:
        pass

    @abstractmethod
    def reserve_book(self, book) -> None:
        pass
