# File for starting the project
from src.app.managers.manager import Manager
from src.app.db import create_db

if __name__ == "__main__":
    create_db()
    manager = Manager()
    manager.run()
