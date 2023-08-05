""" Program to extract the middle letter of the given string, if no middle then return empty string"""


def mid(s):
    if len(s) % 2 == 0:
        print("")
    else:
        f = int(str(len(s) / 2).split(".")[0])
        return f"Middle element of the string is {str(s)[f]}"


middle_number = mid("abc")
print(middle_number)
