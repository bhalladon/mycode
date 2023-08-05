def capital_indexes(string1):
    # list_index_of_capital_letters = []
    # for i in range(len(string1)):
    #     if string1[i].isupper():
    #         list_index_of_capital_letters.append(i)
    # return list_index_of_capital_letters
    return [i for i in range(len(string1)) if string1[i].isupper()]


f = capital_indexes("HelLO")
print(f)

for i, l in enumerate(["a", "b", "c"]):
    print(f"Value at Index {i} is: {l}")

