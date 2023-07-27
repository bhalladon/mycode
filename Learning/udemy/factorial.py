class Factorial:

    def __init__(self):
        factorial_number = int(input("Please enter a integer value to find the factorial: "))
        global var
        var = 1
        for i in range(1, factorial_number + 1):
            var = var * i
        print("Factorial of the number " + str(factorial_number) + " is: " + str(var))


a = Factorial()
# a.print_factorial()
