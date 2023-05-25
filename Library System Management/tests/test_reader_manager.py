from src.app.managers.manager import Manager

FIRST_NAME = "Test"
SURNAME = "Reader"
READER_ID = 1
READER_NUM = 123
EXISTING_NUMS = [999, 555]
LOGIN_OK_PRINT = "Logged in\n"
LOGIN_ERR_PRINT = "Login error\n"


def mock_login(*args):
    if len(args) == 1 and type(args[0]) == int and args[0] == int(READER_NUM):
        return READER_ID
    if len(args) == 2 and args[0] == FIRST_NAME and args[1] == SURNAME:
        return READER_ID
    return None


def mock_register(*args):
    if len(args) == 3 and args[0].isnumeric() and int(args[0]) not in EXISTING_NUMS:
        return READER_ID
    return None


def test_login_correct_number(capfd, mocker, monkeypatch):
    mocker.patch('src.app.db.reader.ReaderDB.login', mock_login)
    monkeypatch.setattr('builtins.input', lambda x: str(READER_NUM))
    manager = Manager()
    manager.login()
    out, err = capfd.readouterr()
    assert out == LOGIN_OK_PRINT
    assert manager._reader == READER_ID


def test_login_correct_names(capfd, mocker, monkeypatch):
    mocker.patch('src.app.db.reader.ReaderDB.login', mock_login)
    monkeypatch.setattr('builtins.input', lambda x: f"{FIRST_NAME} {SURNAME}")

    manager = Manager()
    manager.login()
    out, err = capfd.readouterr()
    assert out == LOGIN_OK_PRINT
    assert manager._reader == READER_ID


def test_login_incorrect_number(capfd, mocker, monkeypatch):
    mocker.patch('src.app.db.reader.ReaderDB.login', mock_login)
    monkeypatch.setattr('builtins.input', lambda x: "124")
    manager = Manager()
    manager.login()
    out, err = capfd.readouterr()
    assert out == LOGIN_ERR_PRINT
    assert manager._reader is None


def test_login_incorrect_only_first_name(capfd, mocker, monkeypatch):
    mocker.patch('src.app.db.reader.ReaderDB.login', mock_login)
    monkeypatch.setattr('builtins.input', lambda x: f"{FIRST_NAME}")

    manager = Manager()
    manager.login()
    out, err = capfd.readouterr()
    assert out == LOGIN_ERR_PRINT
    assert manager._reader is None


def test_login_incorrect_only_surname(capfd, mocker, monkeypatch):
    mocker.patch('src.app.db.reader.ReaderDB.login', mock_login)
    monkeypatch.setattr('builtins.input', lambda x: f"{SURNAME}")

    manager = Manager()
    manager.login()
    out, err = capfd.readouterr()
    assert out == LOGIN_ERR_PRINT
    assert manager._reader is None


def test_login_incorrect_wrong_input(capfd, mocker, monkeypatch):
    mocker.patch('src.app.db.reader.ReaderDB.login', mock_login)
    monkeypatch.setattr('builtins.input', lambda x: f"%sadk1213")

    manager = Manager()
    manager.login()
    out, err = capfd.readouterr()
    assert out == LOGIN_ERR_PRINT
    assert manager._reader is None


def test_logout_(mocker, monkeypatch):
    mocker.patch('src.app.db.reader.ReaderDB.login', mock_login)
    monkeypatch.setattr('builtins.input', lambda x: str(READER_NUM))
    manager = Manager()
    manager.login()
    assert manager._reader == READER_ID
    manager.logout()
    assert manager._reader is None
    

def test_register(capfd, mocker, monkeypatch):
    def mock_input(x):
        if x == "reader number: ":
            return str(READER_NUM)
        if x == "first name: ":
            return FIRST_NAME
        if x == "surname: ":
            return SURNAME
        return ""
    mocker.patch('src.app.db.reader.ReaderDB.register', mock_register)
    monkeypatch.setattr('builtins.input', mock_input)
    manager = Manager()
    manager.register()
    out, err = capfd.readouterr()
    assert out == "Registered and logged in\n"
    assert manager._reader == READER_ID


def test_should_not_register_if_number_exists(capfd, mocker, monkeypatch):
    def mock_input(x):
        if x == "reader number: ":
            return str(EXISTING_NUMS[0])
        if x == "first name: ":
            return FIRST_NAME
        if x == "surname: ":
            return SURNAME
        return ""
    mocker.patch('src.app.db.reader.ReaderDB.register', mock_register)
    monkeypatch.setattr('builtins.input', mock_input)
    manager = Manager()
    manager.register()
    out, err = capfd.readouterr()
    assert out == "Registration error\n"
    assert manager._reader is None


def test_should_not_register_if_wrong_number(capfd, mocker, monkeypatch):
    def mock_input(x):
        if x == "reader number: ":
            return "basjhd%@^ds"
        if x == "first name: ":
            return FIRST_NAME
        if x == "surname: ":
            return SURNAME
        return ""
    mocker.patch('src.app.db.reader.ReaderDB.register', mock_register)
    monkeypatch.setattr('builtins.input', mock_input)
    manager = Manager()
    manager.register()
    out, err = capfd.readouterr()
    assert out == "Registration error\n"
    assert manager._reader is None
