print("Please enter 1 for list:")
print("Please enter 2 for tuple:")
print("Please enter 3 for sets:")
print("Please enter 4 for Dictionary:")
def take_input():
    try:
        global var
        var = int(input("Enter your choice:"))

    except ValueError:
        print("Please enter an integer.")
        take_input()

    print(var)

take_input()
if var == 1:
    list1 = []
    for x in range(5):
        list1.append("hello")
    print (list1)

elif var == 2:
    tuple1 = (1,2,3,4,5)
    print(tuple1)

elif var ==3:
    set1 = set([1,2,3,4,5])
    print(set1)

elif var == 4:
    dict1 ={'name': "rajiv",
              'last name':"bhalla"}
    print(dict1)
    dict1.update({'name': "Manila"})
    print(dict1)
