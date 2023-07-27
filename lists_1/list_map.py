from functools import reduce
f = lambda a,b: a+b

y = list(map(f, [1, 2, 3, 4], [5, 6, 7, 8]))
print(y)

y = [a+b for a in range(1,11) for b in range(11,21)]
print(y)

f = list(filter(lambda x: x>20, y))
print(f)

f = list(map(lambda a: a**2, range(4)))
print(f)

f = list(filter(lambda a: a<9, range(14)))
print(f)

f = list(map(lambda a,b,c: a+b+c, range(1,6), range(6,11), range(11,16)))
print(f)

usernames = ["rajiv", "abhishek", "desh", "sanket"]
print(sorted(usernames))

list1 = [1,2,3,4]
list2 = [5,6,7,8]
list1.append(list2)
print(list1)
list1.extend(list2)
print(list1)


