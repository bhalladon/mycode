#program to convert list to a string
def list_to_str():
    list_test = ["hello", "world", "beautiful"]
    str_test = " ".join(list_test)
    print(str_test)

    # convert string to list
    list_test1 = str_test.split(" ")
    print(list_test1)


def fetch_domainame():
    list_dom = ["www.google.com", "www.gmail.com", "www.yahoo.dev.com"]
    for x in list_dom:
        f = x.split(".")[-2]
        print(f)


def reverse(sentence):
    sen = []
    for x in range(len(sentence)):
        sen += sentence[len(sentence) - x - 1]
    print("".join(sen))


def fibonnaci(sequence):
    n1,n2 = 0,1
    for x in range(sequence):
        print(n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth


# list_to_str()
# fetch_domainame()
# reverse("bhalla")
fibonnaci(6)

list12=["chakde", "india"]
print(" ".join(list12))
