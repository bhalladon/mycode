# program to find the factorial of a number

def take_input(var):
    factorial=1
    for x in range(1, var+1):
        factorial = factorial*x
    print(factorial)

take_input(6)