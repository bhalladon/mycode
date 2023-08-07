"""
program to check given string is palindrome or not
"""


def palindrome(s: str) -> bool:
    original_string = s
    reversed_string = ""

    for i in range(0, len(s)):
        reversed_string += s[len(s) - i - 1]

    print(f"Reversed string is: {reversed_string}")

    if original_string.lower() == reversed_string.lower():
        return True
    else:
        return False


assert bool(palindrome("madam")) is True
