def take_input():
    try:
        global var1, var2
        var1 = str(input("Please enter first string:  "))
        var1 = var1.lower()
        var2 = str(input("Please enter second string:  "))
        var2 = var2.lower()
    except ValueError:
        print ("Please enter string. Try Again")
        take_input()

take_input()

str1_len = len(var1)
str2_len = len(var2)

str1_list=[]
str2_list=[]
for i in range(str1_len):
    str1_list += var1[i]
for i in range(str2_len):
    str2_list += var2[i]

for items in str2_list:
    if items in str1_list:
        pass
    else:
        print("two strings are not anagram")
        exit(0)

print("Two strings are anagram")