def factorial():
    number = int(input("Enter a integer number to find factorial: "))
    factorial = 1
    for i in range(1,number+1):
        factorial = factorial * i
    print (factorial)


factorial()