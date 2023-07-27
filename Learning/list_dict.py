

a = [1,2,3,4]
a.insert(0, 5)
a.remove(4)
print a

##dictionary_atom

b = {'a':1,'b':2}
print b['a']
print b['b']
try:
    print b['c']
except KeyError:
    print "chakde"

b['a'] = 2
print b['a']
del b['a']
print b