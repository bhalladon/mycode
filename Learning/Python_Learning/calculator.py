#!/usr/bin/python

print "Welcome to Calculator, It can perform operations like addition, \
subtraction, multiplication, division etc.."
         
while True:
    print "\nPlease select an operation to perform:"
    print "\n1) Enter 'add' to add two numbers"
    print "2) Enter 'subtract' to subtract two numbers"
    print "3) Enter 'multiply' to multiply two numbers"
    print "4) Enter 'divide' to divide two numbers"
    print "5) Enter 'quit' to end the program"
    user_input = str(raw_input("\nEnter your choice: "))
    
    if user_input.strip() == "quit":
        break
    
    elif user_input.strip() == "add":
        first_num = float(input("Enter first number:"))
        second_num = float(input("Enter Second number:"))    
        result = str("The sum of two numbers are: ")+ str(first_num + second_num)
        print "\n"+result+"\n"
    
    elif user_input.strip() == "subtract":
        first_num = float(input("Enter first number:"))
        second_num = float(input("Enter Second number:"))
        result = str("The subtraction of two numbers are: ")+ str(first_num - second_num)
        print "\n"+result+"\n"
    
    elif user_input.strip() == "multiply":
        first_num = float(input("Enter first number:"))
        second_num = float(input("Enter Second number:"))
        result = str("The multiplication of two numbers are: ")+ str(first_num * second_num)
        print "\n"+result+"\n"
    
    elif user_input.strip() == "divide":
        first_num = float(input("Enter first number:"))
        second_num = float(input("Enter Second number:"))
        result = str("The division of two numbers are: ")+ str(first_num / second_num)
        print "\n"+result+"\n"
    
    else:
        print "\nunknown operation selected.\n"
    
    