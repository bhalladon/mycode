import re

def reverse_each_word(sentence):
    str_to_rev_list = list(sentence)
    # STEP1: To check if there is any special character (spaces, punctuation) in the string or not
    # If no special character go ahead reversed the string
    pattern = "[^0-9a-zA-Z]"
    g = re.findall(pattern, sentence)
    if not g:
        str2 = []
        rev_string = ""
        for x in range(len(sentence)):
            str2.append(sentence[len(sentence) - 1 - x])
        str2 = list(str2)
        return rev_string.join(str2)

    # STEP1: calculate special characters and stored them in a dictionary along with their index values
    special_characters = {}
    for i in range(0, len(sentence)):
        if sentence[i].isalpha() or sentence[i].isdigit():
            continue
        else:
            special_characters.update({i: sentence[i]})
    # print(special_characters)

    # STEP2: Convert string to a list and remove special characters
    store_index = []
    new_list = []
    for i in range(0, len(str_to_rev_list)):
        if not str(str_to_rev_list[i]).isalnum():
            if not store_index:
                new_list.append(str_to_rev_list[0:i])
                store_index.append(i+1)
            else:
                new_list.append(str_to_rev_list[store_index[0]:i])
                store_index.pop(0)
                store_index.append(i+1)

    new_list.append(str_to_rev_list[store_index[0]:])
    # print("new list is: " + str(new_list))

    # STEP3: Now reverse the list new_list
    str2 = []
    rev_string = ""

    for item in new_list:
        for x in range(len(item)):
            str2.append(item[len(item) - 1 - x])
        str2.append(" ")
    str2 = list(str2)
    #print("reversed string is: " + str(str2))

    # STEP4: Remove all white spaces and special characters
    x = re.sub("\s", "", rev_string.join(str2))
    new_x = re.sub("[^0-9a-zA-Z]+", "", x)
    new_x = list(new_x)

    # STEP5: Add white spaces and special characters from the dictionary we created at first step
    for i in special_characters.keys():
        new_x.insert(i, special_characters[i])
    return rev_string.join(new_x)


def main():
    test_str = "String;   2be reversed..."
    assert reverse_each_word(test_str) == "gnirtS;   eb2 desrever..."
    print("String successfully reversed. Spaces, Puntuation are not reversed")
    print("Original string is: " + test_str)
    print("Reversed string is: " + reverse_each_word(test_str))
    return 0


if __name__ == "__main__":
    main()
