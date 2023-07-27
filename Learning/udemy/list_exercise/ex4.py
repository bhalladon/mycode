# program to get the smallest number in a list

list1 = [1,3,1,10,-5]
max = list1[0]

for a in list1:
    if a < max:
        max = a
print(max)
