class CommonFunction():

    def __init__(self):
        var = input("Please choose a function to perform:\
        \na) Fibonnaci,\
        \nb) Factorial,\
        \nc) Reverse a string,\
        \nd) Palindromes,\
        \nPlease enter your choice: ")

        var = str(var).lower()
        if var == "a":
            CommonFunction.fibonnaci(self)

        if var == "b":
            CommonFunction.factorial(self)

        if var == "c":
            CommonFunction.reverse_string(self)

        if var == "d":
            CommonFunction.palindromes(self)

        if var not in ["a","b","c","d"]:
            print ("Please enter a valid choice.")
            CommonFunction.__init__(self)

    def fibonnaci(self):
        var = int(input("Please enter a positive number for the fibonacci sequence: "))
        n1 = 0
        n2 = 1
        for i in range(var):
            print(n1)
            nth = n1 + n2
            n1 = n2
            n2 = nth

    def factorial(self):
        var = int(input("Please enter an integer value to find the factorial of a number: "))
        factorial = 1
        for i in range(1, var + 1):
            factorial = factorial * i

        print(factorial)

    def reverse_string(self):
        var = str(input("Enter a string to reverse: "))
        rev_string = []
        new_str=()
        for i in range(len(var)):
            rev_string.append(var[len(var) - i - 1])
        print("".join(str(x) for x in rev_string))

    def palindromes(self):
        try:
            var = str(input("Please Enter a string:  "))
            var = var.lower()
            # if var <= 0:
            #     print ("Please enter a positive number: Try again")
            #     take_input()
        except ValueError:
            print("Please enter a string only. Try Again")
            CommonFunction.palindromes()

        length_str = len(var)
        rev_string = []

        for x in range(length_str):
            rev_string += var[length_str - 1]
            length_str = length_str - 1

        new_str = ""
        for i in rev_string:
            new_str += i

        if var == new_str:
            print("The string you entered is a palindrome.")
        else:
            print("The string you entered is not a palindrome.")


if __name__ == "__main__":
    a = CommonFunction()
