x = [123, 456, 719, 668, 1024, 657,104]
list1 = []
dup_rem = []
new = []
dict1 = {}

for i in x:
    z = str(i)
    list1.append(z[1])
    if list1[-1] in dict1: # To check if the item already exits in dict1 or not
        if dict1[z[1]] > i:
            dict1[z[1]] = [i, dict1[z[1]]]
        else:
            dict1[z[1]] = [dict1[z[1]], i]
    else:
        dict1[z[1]] = i

# Remove duplicates from list
for item in list1:
    if item in dup_rem:
        pass
    else:
        dup_rem.append(item)

# sort new list
for i in range(len(dup_rem)):
    for j in range(i + 1, len(dup_rem)):
        if dup_rem[i] > dup_rem[j]:
            dup_rem[i], dup_rem[j] = dup_rem[j], dup_rem[i]

for i in dup_rem:
    new.append(dict1[i])
print("Original list is: ")
print(x)
print("Sorted list is: ")
print(new)




