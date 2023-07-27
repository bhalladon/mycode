#!/usr/bin/python

def data():
    try:
        text = str(input("Enter a string:"))  # Taking a string from the user
        while (text == "") or (
                text.strip() == ""):  # If user enters nothing or white-spaces only then it again ask for user input
            print("Please enter a string.")
            text = str(input("Enter a string:"))  # Prompt for user input
    except ValueError:
        print("Please enter a string.")
    text = text.lstrip()
    text = text.rstrip()

    b = open("newfile.txt", "a")
    b.write(text + "\n")  # Write to the file (append to the file if "newfile.txt" already existing
    b = open("newfile.txt", 'r')  # Read the file
    print(b.read())
    b.close()  # Closed the file


data()
