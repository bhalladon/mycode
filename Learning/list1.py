# list1 = ["rajiv||1", "rajiv||2", "rajiv||3"]
#
# for x in list1:
#     if x.__contains__("||"):
#         while "x" in list1:
#             list1.remove("||")


# list1 = ["a","b","c","d","e","f"]
# print(list1[1:4])
#
# print(type(list(list1)))
#
# list2=["abc", "bhalla", "dhd"]
# list3=[]
# for items in list2:
#         list3 += items[0]
# print(list3)

# list_original = [1, 2, 4, 5, 2, 5, 6, 3, 5, 1, 3]
# list_unique = []
# list_duplicate = []
# for i in list_original:
#     if i not in list_unique:
#         list_unique.append(i)
#     else:
#         print("Dup value is: " + str(i))
#         list_duplicate.append(i)
# print(list_duplicate)
#
# # print true if first and last elements in a list are divisible  by 4
#
# list = [4,9,0,16]
# if (list[-1] % 4) == 0 and (list[0] % 4) == 0:
#     print("divisible by 4")
# else:
#     print("Not divisible by 4")
#
# # prog to print sum of all elements in a list
# list_sum = [3,3,3,5]
# sum=0
# for i in list_sum:
#     sum+=i
# print(sum)

# prog to find max number in a list
# list_max = [15, 50, 100, 5,20]
# max=0
# for i in list_max:
#     if i > max:
#         max=i
# print (max)


# len_list = len(list_max)
# max_num=""
# for i in range(len_list):
#     if len_list - i != 1:
#         if list_max[i] > list_max[i+1]:
#             list_max[i+1] = list_max[i]
#         else:
#             pass
# print(list_max)
# print(list_max[-1])

str1="bhalla"
print(eval(repr(str1)))
