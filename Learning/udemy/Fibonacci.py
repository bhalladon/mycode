class Fibonacci:

    def __init__(self):
        sequence_length = int(input("Please enter the length of the sequence for fibonacci series: "))
        n1 = 0
        n2 = 1
        fib_series= []
        for i in range(sequence_length):
            print(n1)
            nth = n1 + n2
            n1 = n2
            n2 = nth

a = Fibonacci()