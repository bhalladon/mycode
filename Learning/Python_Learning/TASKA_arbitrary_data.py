#!/usr/bin/python

def data1():
    
    text = None
    while text is None or (text == "") or (text.strip() == ""):
        try:
            text = str(raw_input("Enter a string:")) ## Taking a string from the user
        except ValueError:
            print "Please enter a string:"
            
    text = text.lstrip() ## Remove white-spaces if any before the string
    text = text.rstrip() ## Remove the white-spaces if any after the string
        
    b = open("newfile.txt", "a")
    b.write(text + "\n") ## Write to the file (append to the file if "newfile.txt" already existing
    b = open("newfile.txt", 'r') ## Read the file 
    
    print b.read() ## Print the file contents of newfile.txt
    
    b.close() ## Closed the file
    
data1()