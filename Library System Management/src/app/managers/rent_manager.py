from src.app.utils import list_to_console
from src.app.db.rent import RentDB
from src.app.db.reservation import ReservationDB


class RentManager:
    COMMANDS = {"logged": ["rent", "rented_books", "return_book", "rent_history"]}

    def rent(self):
        book_id = input("Book id: ")
        if not self._reader:
            print("Please log in")
            return
        if self.reader.fines > 0.0:
            print("You cannot rent any more books. Please pay off your fines")
            return
        available = RentDB.check_availability(book_id)
        if available is None:
            print("Book not found")
        if available <= 0:
            print("Book not available")
            return
        if RentDB.check_if_rented(self._reader, book_id):
            print("You already have this book")
            return
        if ReservationDB.check_if_reserved(self._reader, book_id):
            print("Book is reserved")
            return
        rent = RentDB.rent(self._reader, book_id)
        if rent:
            print("Book rented")

    def rented_books(self):
        if not self._reader:
            print("Please log in")
            return
        rents, rents_display = RentDB.get_active_rents(self._reader)
        list_to_console(rents_display)
        return rents

    def rent_history(self):
        if not self._reader:
            print("Please log in")
            return
        rents, rents_display = RentDB.get_historical_rents(self._reader)
        for rent in rents_display:
            print(rent)
        return rents

    def return_book(self):
        rents = self.rented_books()
        sel = int(input("Which book you want to return?: "))
        rent = rents[sel]
        book_id = rent.book_id
        fine = RentDB.calc_fine(rent)
        if fine > 0.0:
            RentDB.create_fine_notification(rent.reader_id, fine)
            RentDB.charge_fine(rent.reader_id, fine)
        if RentDB.return_book(rent.id):
            RentDB.create_notifications_for_reservations(book_id)
            print("returned")
        else:
            print("cannot return")
