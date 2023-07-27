"""print factorial of a number"""
def take_input():
    try:
        global var
        var = int(input("Please enter a numeric number to find the factorial: "))
        if var <= 0:
            print ("Please enter a positive number: Try again")
            take_input()
    except ValueError:
        print ("Please enter a numeric number only. Try Again")
        take_input()

take_input()
factorial = 1
for x in range(1,var+1):
    factorial = factorial*x
print(factorial)