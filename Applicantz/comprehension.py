# List comprehension:
y = [i for i in range(100) if i % 3 == 0]
print(y)

# dict Comprehension

dict1 = {i: f"item{i}" for i in range(1, 100) if i % 20 == 0}
print(dict1)

# for items in dict1.values():
#     print(items)

dict1[20] = "rajiv"
print(dict1[20])

l = [1, 2, 3, 4, 4, 2, 2]
dup_items = []
for ele in l:
    if l.count(ele) > 1 and ele not in dup_items:
        dup_items.append(ele)
print(dup_items)

d = []
for i in range(len(l)):
    for j in range(i + 1, len(l)):
        if l[i] == l[j] and l[i] not in d:
            d.append(l[i])

print(d)

data = {'jay': [1, 2, 3], "bhal": "hey", "hye": [4, 5, 6]}
count = 0
for item in data:
    if isinstance(data[item], list):
        count = count + 1

print(count)

vowels = ["a", "e", "i", "o", "u"]
count = 0
string1 = "hellao"

for char in string1:
    if char in vowels:
        count = count + 1

print(count)

# Reverse a string
string1 = "reverse"
new_string = []
for i in range(len(string1)):
    new_string.append(string1[len(string1) - i - 1])


print("".join(new_string))
