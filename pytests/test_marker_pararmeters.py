import pytest

@pytest.mark.parametrize("username, password", [("selenium", "selenium123"), ("api","api123"), ("webui","webui123")])
def test_login(username,  password):
    print(username)
    print(password)
