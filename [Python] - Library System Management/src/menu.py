class Menu:
    def display_user_menu(self):
        print("Welcome to Library!:\n1. Log out \n2. Display books in library \n3. Borrow book"
              " \n4. Display all your books \n5. Return book \n6. Reserve book"
              " \n7. Display all your reserved books")

    def display_menu(self):
        print("Welcome to Library!:\n1. Log in \n2. Register \n3. List all events \n4. Exit")

    def get_username(self):
        username = input("Enter your username: ")
        return username

    def get_password(self):
        password = input("Enter your password: ")
        return password
