class bhalla():
    def __init__(self):
        print("This is init function")

    def __call__(self, *args, **kwargs):
        print("This is call function")

if __name__ == "__main__":
    bhalla()