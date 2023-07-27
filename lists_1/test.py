var = str(input("enter a number:"))
rev = []
for x in range(len(var)):
    rev += var[len(var) -x -1]
print(rev)
f = "".join(rev)
if f == var:
    print("it is a palindrome")
else:
    print("not a palindrome")

# import requests, xml
# headers = {"application-type:"}
# params ={"name":"rajiv", "age":34}
# f = requests.get("POST", url = "", data = params, headers=headers)
#     assert f.status_code == 200
#     f = json(f.text)[]
#
#
# from selenium import webdriver
#
# driver = webdriver.Chrome(executable_path="./Chomedriver.exe")
#
# driver.get(url)
# username = driver.find_element_by_name("username")
# username.click()
# username.send_keys("abc")
# password = driver.find_element_by_id("password")
# password.click()
# password.send_keys("blabla")
# driver.find_element_by_name("submit").click()
#
# if driver.find_element_by_name("test12"):
#     print("login successfull")
# else:
#     print("login is unsuccessfull")
#
# /div/ksd/ds
#
# chmod filename 700
# 777 +x















