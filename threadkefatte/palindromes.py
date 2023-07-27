""" program to check wheather a string is palindrome or not """
def take_input():
    try:
        global var
        var = str(input("Please Enter a string:  "))
        var = var.lower()
        # if var <= 0:
        #     print ("Please enter a positive number: Try again")
        #     take_input()
    except ValueError:
        print ("Please enter a string only. Try Again")
        take_input()

take_input()

length_str = len(var)
rev_string=[]

for x in range(length_str):
    rev_string +=var[length_str -1]
    length_str = length_str -1

new_str = ""
for i in rev_string:
    new_str += i
print (new_str)

if var == new_str:
    print ("The string you entered is a palindrome.")
else:
    print ("The string you entered is not a palindrome.")
