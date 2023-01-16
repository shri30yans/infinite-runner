s = "abcdefghijk"
s = "".join([str.upper(x) if num%2 else x for num,x in enumerate(s)])
print(s)