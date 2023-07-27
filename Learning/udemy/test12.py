#### program to sort a list without sorting function

list1 = [7, 5, 3,8,2,1,9]
print(sorted(list1))
list2 = len(list1)

new_list=[]
try:
    for i in range(list2):
        if list1[i] > list1[i+1]:
            list1[i], list1[i+1] = list1[i+1], list1[i]
        print(list1)

except IndexError:
    pass
print (list1)

# print (new_list)