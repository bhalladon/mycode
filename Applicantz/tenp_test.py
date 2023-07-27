factorial = 1
for i in range(1, 6):
    factorial = factorial * i

print(factorial)

### Fibonacci
n1, n2 = 0, 1
for i in range(7):
    print(n1)
    nth = n1 + n2
    n1 = n2
    n2 = nth

# Lamba Expressions
# print 1st ten even numbers

x = lambda i: i * 2
print(x(2))

# List comprehension

x = [i for i in range(2, 21) if i % 2 == 0]
print(x)

# reverse a string
string = "hello"
rev_str = []
for i in range(len(string)):
    rev_str += string[len(string) - i - 1]

print("".join(rev_str))

strin1 = "chakde"
new_string = []
for i in range(len(strin1)):
    new_string += strin1[i]
print(new_string)
