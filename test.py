import os


d = {}
if 0 not in d:
    d[0] = [1]
d[0].append(2)

for i in d:
    print( i, d[i])