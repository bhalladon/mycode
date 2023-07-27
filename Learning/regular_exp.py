import re

# text_to_search = ''' hello 123
# chakde
# india
# aaja mere pass'''
#
# print ('\ttab')  # \t used as actual tab here
# print(r'\ttab')  # with use of 'r' \t is used a normal string

# pattern = re.compile('^ h')
# # print (pattern)
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)

# email = input("Please enter an email address")
# pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
# if re.search(pattern,email):
#     print("Valid email")
# else:
#     print("Not a valid email")


text_to_search1 = "aaja shaam hone aayi\n\
mausam ne li 1angdali2 bhalladon@gmail.com abc@yaghoo.com"
pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|net|org|edu)"
pattern_to_find_digits = "\d"
pattern_to_find_nondigits = "\D"

f = re.findall(pattern, text_to_search1)
print (f)