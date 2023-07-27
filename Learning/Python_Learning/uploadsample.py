#!/usr/bin/python

import os

fp = os.path.join(os.getcwd(),"/home/bhalla/Desktop/Projects/MA/Pythonproject/samples")
file1 =  os.listdir(fp)

for entry in file1:
    print fp+"/"+entry


