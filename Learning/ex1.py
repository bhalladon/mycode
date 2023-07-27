def reverse_each_word(sentence):
    # TODO: Implement this function
    total_length = len(sentence)
    rev_string = []
    str_rev_string = ""
    for i in range(total_length):
        rev_string += sentence[total_length - 1]
        total_length = total_length - 1
    print(str_rev_string.join(rev_string))
    return

def main():
    test_str = "String;   2be reversed..."
    f = reverse_each_word(test_str)
    print(f)
    print("")
    assert reverse_each_word(test_str) == "gnirtS;   eb2 desrever..."
    return 0

main()