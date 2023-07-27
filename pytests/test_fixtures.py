import pytest
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

driver = None
@pytest.fixture()
def setup():
    global driver
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver.maximize_window()
    yield
    driver.quit()
    print("closing the browser")

def test_1(setup):
    driver.get("https://www.gmail.com")
    print("Test 1executed")

def test_2(setup):
    driver.get("https://www.facebook.com")
    print("Test 2 executed")