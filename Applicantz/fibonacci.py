def fibonacci(sequence_len):
    #sequence_len = int(input("please enter the sequence length: "))
    n1,n2 = 0,1
    for x in range(sequence_len):
        print (n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth
fibonacci(5)