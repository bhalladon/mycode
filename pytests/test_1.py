def test_first():
    x=10
    y=10
    assert x==y

def test_second():
    name="Selenium"
    title="Selenium is a webdriver"
    assert name in title

def test_three():
    name="Jenkins"
    title="jenkins is CI server"
    assert name in title, "title does not match"

