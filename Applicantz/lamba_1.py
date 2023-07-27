# print first ten numbers using lambda

x = lambda a: a * a
f = map(x,[4,5,6])
print(list(f))

# def func(n):
#     return n*n
#
#
# x = lambda a: func(a)
# print(x(2))
#
# x = lambda a,b: a + b
# print(x([1,2,3],[4,5,6]))
#
# list1 = ["a", "b", "c", "d", "e", "f"]
# list2 = ["g","h","i","j","k","l"]
# print(list1 + list2)
#
#
# x = lambda a: a % 4 == 0
# f = filter(x,range(1,41))
# print(list(f))
#
# x = lambda a,b : a % b != 0
# f = filter(x,4,3)
# print (list(f))


