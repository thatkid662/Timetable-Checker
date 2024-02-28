import re
a = [1, 2]
c = "{a[0 if 69 == 0 else 1]} abcd {a[0]}"
b = re.findall(r"{([^}]*)}", c)
print(b)
for content in b:
    print(content)
    e = eval(content, {"a": a})
    print(e)
    c = c.replace("{" + str(content) + "}", str(e))
print(c)

#print(str.format(c, a=a))
"""p = f"{a[0 if 1 == 0 else 1]}"
print(p)
b = str.format(p, a = a)
print(b)"""