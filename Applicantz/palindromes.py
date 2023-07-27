srin="bhalla"
rev = srin[::-1]
print(rev)
def palindromes():
    pal_string = str(input("Enter a string or word to check if it palindrome or not: "))
    rev_string = []
    rev_string1=""
    for x in range(1, len(pal_string)+1):
        rev_string += pal_string[len(pal_string) - x]
    if str(rev_string1).join(rev_string) == pal_string:
        print("String entered is a palindrome")
    else:
        print("String entered is not a palindrome")
# palindromes()