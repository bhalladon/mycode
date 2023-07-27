# program o reverse a sring

str1="bhalla"
str2=[]
rev_string=""
for x in range(len(str1)):
    str2.append(str1[len(str1) -1 -x])
print(rev_string.join(str2))
