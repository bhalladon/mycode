# Python program to get a list, sorted in increasing
# order by the last element in each tuple from a given
# list of non-empty tuples

list1 = [(2,3),(2,1),(2,5)]

for i in range(len(list1) - 1):
    for j in range(len(list1) -i -1):
        if list1[j][-1] > list1[j+1][-1]:
            list1[j], list1[j+1] = list1[j+1], list1[j]
print(list1)
