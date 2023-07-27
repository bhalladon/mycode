list1 = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','jack']

print(list1[2:-3])
print(list1[2:5])
print(list1[0:])
print(list1[4:-2])
print(list1[4:6])
print(list1[1::2])

list2=[]
for i in list1:
    if i.startswith("j"):
        list2.append(i)
print(list2)

import time
print(time.ctime())
print(time.asctime())

print (id(list2))
del list2
try:
    print (id(list2))
except NameError:
    print("List2 does not exist.")