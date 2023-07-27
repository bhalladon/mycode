class Reverse_number:

    def __init__(self):
        str_to_reverse = str(input("Please enter a string to reverse: "))
        total_length = len(str_to_reverse)
        rev_string=[]
        str_rev_string = ""
        for i in range(total_length):
            rev_string+=str_to_reverse[total_length - 1]
            total_length = total_length - 1
        print(str_rev_string.join(rev_string))


a = Reverse_number()
