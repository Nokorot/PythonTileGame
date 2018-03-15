
x = {}
x[1] = ['c', 'd']
x[2] = ['e', 'f']
x[0] = ['a', 'b']

def iter():
    for l in x.values():
        for e in l:
            yield e;

for e in iter():
    print e
