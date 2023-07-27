import re
text1 = "Theaindia"
text2 = "The aisan faramosh india"

pattern = "^The.*india$"
f = re.search(pattern, text2)
print(f)

pattern="[a-zA-Z0-9@[a-z]]+@"

g = re.sub(pattern,"bhalla",text2)
print(g)
