# def new(a):
#     return a + 3
#
# f = map(new,(1,2,3,4,5))
# print(tuple(f))
#
# x = map(lambda a: a + 5, [1,2,3,4,5])
# print(list(x))
#
# def new1(a,b):
#     return a + b
#
# f = map(new1,[1,2,3,4],[5,6,7,8])
# print(list(f))

def fibonacci(sequence_len):
    #sequence_len = int(input("please enter the sequence length: "))
    n1,n2 = 0,1
    for x in range(sequence_len):
        print (n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth

f = map(fibonacci, (5,7,9))
print(f)