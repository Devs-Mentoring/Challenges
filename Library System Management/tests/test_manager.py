from src.app.managers.manager import Manager


def test_join_commands_should_return_a_list_of_all_possible_commands():
    manager = Manager()
    commands = manager.join_commands()
    counter = 0
    for command_type in commands:
        counter += len(commands[command_type])
    assert counter == 17


def test_available_commands_should_return_a_list_of_commands_for_unlogged_user():
    expected = {'add_book', 'login', 'register', 'exit'}
    manager = Manager()
    manager._reader = None
    commands = set(manager.available_commands())
    assert len(commands) == 8
    assert expected.issubset(commands)


def test_available_commands_should_return_a_list_of_commands_for_logged_user():
    expected = {"logout", "exit"}
    manager = Manager()
    manager._reader = 1
    commands = set(manager.available_commands())
    assert len(commands) == 14
    assert expected.issubset(commands)


def test_should_display_new_notifications_for_logged_user(capfd, mocker):
    reader_id = 1

    def mock_new(reader):
        return ['message1', 'message2'], ['message1 display', 'message2 display']

    mocker.patch('src.app.db.notification.NotificationDB.new', mock_new)
    mocked_all_read = mocker.patch('src.app.db.notification.NotificationDB.all_read')
    manager = Manager()
    manager._reader = reader_id
    manager.display_new_notifications()
    out, err = capfd.readouterr()
    assert out == "You have new messages:\nmessage1 display\nmessage2 display\n"
    mocked_all_read.assert_called_once_with(reader_id)
