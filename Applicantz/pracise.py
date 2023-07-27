x = lambda a: 3*a + 1
print(x(2))

g = lambda fn, ln: str(fn).strip().title() + " " + str(ln).strip().title()
print (g("   raJiv     ", "         bhalla      "))

h = lambda a,b: a + b
print(h(1,2))

f = map(h, [1,2,3],[4,5,6])
print (list(f))

''' first ten even numbers using lambda'''
def list1(n):
    num_list=[]
    for x in range(1, n+1):
        num_list.append(x)
    return (num_list)

print(list1(5))
print (list(filter(lambda x: (x%2 == 0), list1(31))))

team_names = ["rajiv bhalla", "sanket sharma", "desh bandhu walia", "abhishek junir kalia", "mohit jaggi"]
team_names.sort(key=lambda names: names.split( " ")[-1].lower())
print(team_names)


temp = [("chandigarh", 35.2),("Nakodar",36)]
c_to_f = lambda data: (data[0], (9/5)*data[1] + 32)
print(list(map(c_to_f, temp)))

#to print factorial of a number
var = int(input("Please enter a integer value: "))
fact = 1
for x in range(1,var+1):
    fact = fact * x

print(fact)

# o prin fibonacci series
var = int(input("Enter the sequence length: "))
n1,n2 = 0, 1
for x in range(var):
    print(n1)
    nth = n1 + n2
    n1 = n2
    n2 = nth

# program o reverse a string
var = str(input("Enter a string to reverse: "))
len_str  = len(var)
rev = []
for x in range(len_str):
    rev.append(var[len_str - x - 1])
print(rev)

# program o conver sring ino a lis
var = "hello hpow are ou"
lis = var.split(" ")
print(lis)

lis_sr=("chakde ").join(lis)
print(lis_sr)
#
# #prog to sum all items in a list
# list1= [1,2,3,4,5,6]
# total_sum = 0
# total_mul_sum = 1
# for x in list1:
#     total_sum = total_sum + x
#     total_mul_sum = total_mul_sum * x
# print(total_sum)
# print(total_mul_sum)

# program o ge bigges number in a lis
lis1 = [7,1,9,10,3,35,23,101]
max = lis1[0]

for x in lis1:
    if x > max:
        max = x
print(max)

# program o ge smalles number in a lis
lis1 = [7,1,9,10,3,35,23,0,101]
max = lis1[0]

for x in lis1:
    if x < max:
        max = x
print(max)

list5 = [5,9,10,44,35,23,87,45,67,24,1,2,3]
avg = 7
print (list(filter(lambda x: x < avg, list5)))

squares = [i**2 for i in range(1,11) if i < 5]
print (squares)


lis1= [("Rajiv Bhalla", 36), ("Abhishek Kalia" , 45)]
pung = [name for (name, age) in lis1 if age < 40]
print(pung)

lis1 = [4,5,6]
res = [i*4 for i in lis1]
print(res)

res = lambda a,b: a + b
print(list(map(res, [1,2,4],[5,6])))

lis1=[17,2,3,4]
lis2=[5,6,17,8]
lis3=[11,12,13,14,17]
even = list(filter(lambda  x: x%2 == 0, lis3))
print("eve no are:" + str(even))
lis3.remove(17)
print(lis3)
import sys
print(sys.getsizeof(lis3))
print(dir(list))
print([(a,b,c) for a in lis1 for b in lis2 for c in lis3])
print([(a == b == c) for a in lis1 for b in lis2 for c in lis3])

