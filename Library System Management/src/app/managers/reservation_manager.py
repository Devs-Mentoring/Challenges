from src.app.utils import list_to_console
from src.app.db.rent import RentDB
from src.app.db.reservation import ReservationDB


class ReservationManager:
    COMMANDS = {"logged": ["reserve", "reservations", "cancel_reservation"]}

    def reserve(self):
        book_id = input("Book id: ")
        if not self._reader:
            print("Please log in")
            return
        if RentDB.check_if_rented(self._reader, book_id):
            print("You already have this book")
            return
        if ReservationDB.reserved_by_reader(self._reader, book_id):
            print("You have already reserved this book")
            return
        available = RentDB.check_availability(book_id)
        if available is None:
            print("Book not found")
            return
        if available > 0:
            print("Book is available you don't have to reserve")
            return
        reservation = ReservationDB.reserve(self._reader, book_id)
        if reservation:
            print("Book reserved")

    def reservations(self):
        if not self._reader:
            print("Please log in")
            return
        reservations, reservations_display = ReservationDB.reader_reservations(self._reader)
        list_to_console(reservations_display)
        return reservations

    def cancel_reservation(self):
        reservations = self.reservations()
        sel = int(input("Which reservation you want to cancel?: "))
        if ReservationDB.end_reservation(reservations[sel].id):
            print("cancelled")
        else:
            print("error")
