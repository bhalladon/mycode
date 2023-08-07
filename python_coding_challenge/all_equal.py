"""
All equal
Define a function named all_equal that takes a list and checks whether all elements in the list are the same.

For example, calling all_equal([1, 1, 1]) should return True.
"""


def all_equal(list1) -> bool:
    first_element = list1[0]

    for i in range(len(list1)):
        if list1[i] == first_element:
            if len(list1) - i == 1:
                return True
        else:
            return False


print(all_equal([1, 1, 3, 1, 1]))
