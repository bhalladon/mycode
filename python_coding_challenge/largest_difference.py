"""
Challenge
Min-maxing
Define a function named largest_difference that takes a list of numbers as its only parameter.

Your function should compute and return the difference between the largest and smallest number in the list.

For example, the call largest_difference([1, 2, 3]) should return 2 because 3 - 1 is 2.

You may assume that no numbers are smaller or larger than -100 and 100.
"""


def largest_difference(l: list):
    max_num = l[0]
    min_num = l[0]

    for i in l:
        if i > max_num:
            max_num = i
    for i in l:
        if i < min_num:
            min_num = i
    print(f"Max num is: {max_num}")
    print(f"\nMin Num is: {min_num}")
    return max_num - min_num


print(largest_difference([3, 2, 1, 8]))
