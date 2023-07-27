def take_input():
    try:
        global var
        var = str(input("Please enter a string to reverse: "))
    except ValueError:
        print ("Please enter a numeric number only. Try Again")
        take_input()

take_input()

total_len = len(var)
rev_string=[]
for x in range(total_len):
    rev_string += var[total_len -1]
    total_len = total_len -1

print(rev_string)
