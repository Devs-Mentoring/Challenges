from src.app.managers.reader_manager import ReaderManager
from src.app.managers.book_manager import BookManager
from src.app.managers.rent_manager import RentManager
from src.app.managers.reservation_manager import ReservationManager
from src.app.db.notification import NotificationDB
from src.app.db.rent import RentDB
from src.app.db.reader import ReaderDB

class Manager(ReaderManager, BookManager, RentManager, ReservationManager):
    EXIT_COMMAND = "exit"
    COMMANDS = {"always": [EXIT_COMMAND]}
    ADD_MANAGERS = [ReaderManager, BookManager, RentManager, ReservationManager]

    def __init__(self):
        super().__init__()

    @classmethod
    def join_commands(cls):
        commands_dict = {}
        managers = cls.ADD_MANAGERS + [cls]
        for manager in managers:
            for command_type in manager.COMMANDS.keys():
                commands_dict.setdefault(command_type, [])
                commands_dict[command_type] += manager.COMMANDS[command_type]
        return commands_dict

    def available_commands(self):
        commands_dict = self.join_commands()
        commands = commands_dict['logged'] if self._reader else commands_dict['unlogged']
        commands += commands_dict['always']
        return commands

    def display_new_notifications(self):
        if self._reader:
            notifications, notifications_display = NotificationDB.new(self._reader)
            if len(notifications) > 0:
                print("You have new messages:")
            for notify in notifications_display:
                print(notify)
            NotificationDB.all_read(self._reader)

    def display_reminders(self):
        if self._reader:
            reminders = RentDB.check_for_delays(self._reader)
            fines = ReaderDB.get_fines(self._reader)
            if fines:
                reminders.append(f"!!!You have {fines} PLN unpaid fines. You cannot rent anything else!!!")
            for reminder in reminders:
                print(reminder)

    def display_commands(self):
        commands = self.available_commands()
        str_commands = []
        for _ in range(len(commands)):
            str_commands.append(f"{_}: {commands[_]}")
        if self._reader:
            print(f"{self.reader.first_name} select command")
        print(" | ".join(str_commands))

    def get_command(self):
        self.display_new_notifications()
        self.display_reminders()
        self.display_commands()
        command = int(input())
        available_commands = self.available_commands()
        if not 0 <= command < len(available_commands):
            print("Wrong command")
            return -1
        return available_commands[command]

    def run(self):
        command = ""
        while command != Manager.EXIT_COMMAND:
            command = self.get_command()
            if command != Manager.EXIT_COMMAND:
                eval(f"self.{command}()")
        print("system off")
