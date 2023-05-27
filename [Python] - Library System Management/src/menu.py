def get_password():
    password = input("Enter your password: ")
    return password


def display_user_menu():
    return "Welcome to Library!:\n1. Log out \n2. Display books in library \n3. Borrow book " \
           "\n4. Display all your books \n5. Return book \n6. Reserve book " \
           "\n7. Display all your reserved books \n8. Resign from reservation \nChoose: "


def display_menu():
    return "Welcome to Library!:\n1. Log in \n2. Register \n3. List all events \n4. Exit \nChoose: "


def get_username():
    username = input("Enter your username: ")
    return username


def get_choice(func):
    choice = input(func)
    return choice


def get_title():
    title = input("Title: ")
    return title
