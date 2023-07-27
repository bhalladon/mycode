import time
#string = input("ENTER THE STRING:")

#liststring = list(string)
liststring = ["7", "5", "3"]

len_liststring = len(liststring)
#print len_liststring



for i in range(len_liststring -1):
    print (len_liststring - i - 1)
    for j in range(len_liststring - i - 1):
        #print liststring[j]
        #print liststring[j+1]
        #time.sleep(120)
        if liststring[j] > liststring[j + 1]:
        #print "yes"
            liststring[j], liststring[j + 1] = liststring[j + 1], liststring[j]
    print(liststring)
        #else:
        #    print "no"


new_string=[]
for m in liststring:
    new_string += m

print(new_string, "IS THE STORTED STRING")