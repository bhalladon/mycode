'''
Created on Nov 1, 2016

@author: root
'''

def set_test():
    name = {"rajiv", "ankush", "sunil"}
    age = {12, 14, 56}
    print len(name)
    name.add("brijesh")
    name.add("sunil")
    print(name|age)
    
    test = {1,2,3,5}
    test1 = { 6,7,8,5}
    print str(test & test1).replace('set([', '').replace('])','')
    
    test123 = [123,456,789]
    print test123[0]
        
    

set_test()

