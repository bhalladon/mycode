"""print fibonaaci series"""


def take_input():
    try:
        global var
        var = int(input("Please Enter the length of the sequence: "))
        if var <= 0:
            print ("Please enter a positive number: Try again")
            take_input()
    except ValueError:
        print ("Please enter a numeric number only. Try Again")
        take_input()


take_input()
n1, n2 = 0, 1
#count = 0

#while count < var:
for x in range(var):
    print (n1)
    nth = n1 + n2
    n1 = n2
    n2 = nth
    #count +=1