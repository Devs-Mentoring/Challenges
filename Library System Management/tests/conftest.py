import pytest
from src.app.db import Base


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base
