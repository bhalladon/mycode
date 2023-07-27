# dict1 = {'name': 'Rajiv',
#          'age': 37}
# print(dict1.keys())
# print(dict1.values())
#
# dict2 = {'Fruit_name': ["apple", "mango", "guava","cherry"],
#          'Vege_name': ("lady_finger","Ginger","Locky")}
# print (dict2.keys())
# print(dict2.values())
# print(dict2["Fruit_name"][0])
# print(dict2["Fruit_name"][1])
# print(dict2["Fruit_name"][2])
# print(dict2["Fruit_name"][1:-1])
# del dict2["Fruit_name"][0]
# print (dict2)

dict1 = {2: ("abc","abc1"), 1: "xyz", 7: ("Malaysia", "India")}
dict2 = {2: "chakde", 1: "india", 3: "yahoo"}

# First we make a list containing dictionary keys

dict3=[]
dict4={}

for keys in dict1.keys():
    if keys not in dict2.keys():
        dict3.append(keys)

    for keys in dict2.keys():
        if keys in dict3:
            pass
        else:
            dict3.append(keys)
print (dict3)

######################################################
# ''' program to sort a list and stored it in list "dict3'''
for i in range(len(dict3) - 1):
    for j in range(len(dict3) - i - 1):
        if dict3[j] > dict3[j+1]:
            dict3[j], dict3[j + 1] = dict3[j + 1], dict3[j]

# dict3 = sorted(dict3)
# Now add these
for i in dict3:
    if i in dict1.keys():
        dict4[i]=dict1[i]
        if i in dict2.keys():
            dict4[i]=(dict1[i], dict2[i])
    if i not in dict1.keys():
        dict4[i] = dict2[i]


print (dict4)

