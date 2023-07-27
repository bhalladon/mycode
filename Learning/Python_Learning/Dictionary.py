#!/usr/bin/python

dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'};

dict['Age'] = 8; # update existing entry
dict['School'] = "DPS School"; # Add new entry


print "dict['Age']: ", dict['Age'];
print "dict['School']: ", dict['School'];

print dict; ## print all dictionary items

del dict

#print "dict['Name']: ", dict['Name'];
#print "dict['Age']: ", dict['Age'];