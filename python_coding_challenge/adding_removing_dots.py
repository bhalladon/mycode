"""
Write a function named add_dots that takes a string and adds "." in between each letter.
For example, calling add_dots("test") should return the string "t.e.s.t".

Then, below the add_dots function, write another function named remove_dots that removes all dots from a string.
For example, calling remove_dots("t.e.s.t") should return "test".

If both functions are correct, calling remove_dots(add_dots(string)) should return back the
original string for any string.

(You may assume that the input to add_dots does not itself contain any dots.)
"""


def add_dots(s: str):
    """
    param @s: Enter a string
    return: Response
    """
    # separator = "."
    # new_string = ""
    # for i in range(len(s)):
    #     if len(s) - i == 1:
    #         new_string += s[i]
    #     else:
    #         new_string += s[i] + separator
    new_string = ".".join(s)

    return new_string


def remove_dots(s):
    new_string = str(s).split(".")
    return "".join(new_string)


f = add_dots("hello")
print(f)

g = remove_dots("h.e.l.l.o")
print(g)
