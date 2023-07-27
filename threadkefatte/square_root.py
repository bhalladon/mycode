"""program to find square root of a positive number"""
import itertools
def take_input(var):
    try:
        #global var
        #var = int(raw_input("Please enter a numeric number to find its square root: "))
        if var <= 0:
            print ("Please enter a positive number: Try again")
            take_input(var)
    except ValueError:
        print ("Please enter a numeric number only. Try Again")
        take_input(var)
    for i in itertools.count(1):
        result = var / i
        if result == i:
            print ("square root of the number is: " + str(result))
            break
        else:
            # print result
            pass

take_input(900)

# for i in itertools.count(1):
#     result = float(var/i)
#     if result == i:
#         print "square root of the number is: " + str(result)
#         break
