"""
Boolean and
Define a function named triple_and that takes three parameters and returns True only if they are all True and
False otherwise.
"""


def triple_and(a, b, c):
    if a is True and b is True and c is True:
        return True
    else:
        return False


print(triple_and(a=True, b=True, c=True))
