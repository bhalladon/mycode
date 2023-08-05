""" The goal of this challenge is to analyze a string to check if it contains two of the same letter in a row.
For example, the string "hello" has l twice in a row, while the string "nono" does not have two identical letters
in a row.

Define a function named double_letters that takes a single parameter. The parameter is a string.
Your function must return True if there are two identical letters in a row in the string, and False otherwise."""


def double_letters(s: str) -> bool:
    for i in range(len(s)):
        store_letter = s[i]
        if len(s) - i == 1:
            return False
        elif store_letter == s[i + 1]:
            return True


f = double_letters("s")
print(f)
