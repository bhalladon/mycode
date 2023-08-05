"""
Anagrams
Two strings are anagrams if you can make one from the other by rearranging the letters.

Write a function named is_anagram that takes two strings as its parameters.
Your function should return True if the strings are anagrams, and False otherwise.

For example, the call is_anagram("typhoon", "opython") should return True while the call is_anagram("Alice", "Bob")
should return False.
"""


def is_anagram(s1, s2) -> bool:
    # s1_list = [i for i in s1]
    # print(s1_list)
    for i in range(len(s2)):
        if s2[i] in s1:
            if len(s2) - i == 1:
                return True
        else:
            return False


f = is_anagram("hello", "lllllll")
print(f)
