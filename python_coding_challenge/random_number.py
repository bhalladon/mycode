""" program to generate a random number between 1 and 100 """
import random


def random_number():
    generate_random = random.randint(1, 100)
    return generate_random


get_random_number = random_number()
print(get_random_number)
