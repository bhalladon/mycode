x = [a*b for a in range(1,3) for b in range(3,5)]
print(x)

x = [{a:b*c} for a in range(1,4) for b in range(4,7) for c in range(7,10)]
print(x)
print(type(x[0]))

list1 = ["rajiv" , "abhishek"]
lis2 = ["bhalla", "bkalia"]

for i in range(len(lis2)):
    list1[i] = list1[i]+lis2[i]

print(list1)

