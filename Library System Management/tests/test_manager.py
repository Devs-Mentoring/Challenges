from src.app.managers.manager import Manager


def test_join_commands_should_return_a_list_of_all_possible_commands():
    manager = Manager()
    commands = manager.join_commands()
    counter = 0
    for command_type in commands:
        counter += len(commands[command_type])
    assert counter == 9


def test_available_commands_should_return_a_list_of_commands_for_unlogged_user():
    expected = {'login', 'register', 'find_readers', 'exit'}
    manager = Manager()
    manager._reader = None
    commands = set(manager.available_commands())
    assert commands == expected


def test_available_commands_should_return_a_list_of_commands_for_logged_user():
    expected = {'logout', 'exit'}
    manager = Manager()
    manager._reader = 1
    commands = set(manager.available_commands())
    assert commands == expected

# @classmethod
# def join_commands(cls):
#     commands_dict = {}
#     commands_dict.update(cls.COMMANDS)
#     for manager in cls.ADD_MANAGERS:
#         for command_type in manager.COMMANDS.keys():
#             commands_dict.setdefault(command_type, [])
#             commands_dict[command_type] += manager.COMMANDS[command_type]
#     return commands_dict