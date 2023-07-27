# program to count the number of strings where the string length
# is 2 or more and the first and last character are same from a
# given list of strings.

list1 = ["5445", "3223", "aba", "chakde", "india", "madam"]
ctr = 0

for item in list1:
    if len(item) > 1 and item[0] == item[-1]:
        ctr = ctr + 1

print(ctr)
