list12 = ["a", "b", "c", "d", "e"]
rev_sr = []
rev_str=""
for i in range(len(list12)):
    rev_sr.append(list12[len(list12) - 1 - i])
print(rev_str.join(rev_sr))

newlis=[1,1,3,4,2,3,4,5]
new_list_withoutdup=[]

for i in newlis:
    if i not in new_list_withoutdup:
        new_list_withoutdup.append(i)
print(new_list_withoutdup)
list13=["a","b"]
list12=[2,3,4]
list12.append(5)
print(list12)

list12.append(list13)
print(list12)

list12.extend(list13)
print(list12)