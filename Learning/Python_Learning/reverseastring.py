'''
Created on 26-Feb-2015

@author: rbhalla
'''
import sys

status = True

while status == False:
    try:
        a = int(raw_input("Enter first number"))
        status = True
    except ValueError:
        print "Number is not integer"
        status = False
        a = int(raw_input("Enter first number"))

b = int(raw_input("Enter second number"))

c = a + b
print c


# total_length = 0
# while total_length <= 1:
#     text = str(raw_input("Enter a string to reverse:"))
#     total_length = len(text)
#     if total_length <= 1:
#         print "Please enter a string of length greater than 1:"
#     else:
#         pass
#     
# for x in reversed(range(total_length)):
#     sys.stdout.write(text[x])
    
    
