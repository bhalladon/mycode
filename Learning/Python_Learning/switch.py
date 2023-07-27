#!/usr/bin/python

# define the function blocks
# city = str(raw_input("Enter the city you want to visit: ")).lower()
# known_cities = {"paris": "France",
#                 "rome": "Italy",
#                 "madrid": "Spain"}
# 
# try:
#     print "The city you chose is in ", known_cities[city]
# except KeyError:
#     print "I've never heard of ", city

# map the inputs to the function blocks

def dict():
    while True:
        try:
            num = int(raw_input("Enter a number: "))
        except ValueError:
            print "Please enter a integer value."
            continue
        else:
            break
        
    options = {0 : 'zero',
               1 : 'sqr',
               4 : 'sqr',
               9 : 'sqr',
               2 : 'even',
               3 : 'prime',
               5 : 'prime',
               7 : 'prime',
               }

    try:
        print "The number you entered is "+ options[num]
    except:
        print "Number",num, "not present in our database."
        
dict()