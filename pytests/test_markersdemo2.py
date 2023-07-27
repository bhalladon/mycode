import pytest
import sys

x=5

@pytest.mark.skip
def test_login():
    print("Login")

@pytest.mark.skipif(x<6, reason="python version not supported")
def test_addProduct():
    print("add product")

@pytest.mark.xfail
def test_logout():
    print("Logout done")