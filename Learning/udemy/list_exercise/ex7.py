#Write a Python program to remove duplicates from a list.

list1 = [1, 3, 5, 1, 5]
unique_list=[]

for x in list1:
    if x not in unique_list:
        unique_list.append(x)

print(unique_list)
