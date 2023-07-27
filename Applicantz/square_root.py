import itertools
def squareroot():
    square_root_number = int(input("Please enter a number to find its square root: "))
    for i in itertools.count(1):
        square_root = square_root_number / i
        if i == square_root:
            print("Square root of the number " + str(square_root_number) + " is: " + str(i))
            break
        if i >= square_root_number:
            print ("square root not found.")
            break

squareroot()