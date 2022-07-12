from sys import argv


if len(argv) < 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit()
    
    
four = list()

c = open(argv[1])
st = c.readlines()
for i in range(len(st)):
    st[i] = st[i].strip()
something = st[0].split(",")
for i in range(1, len(something)):
    four.append(something[i].strip())

st = st[1:]


def get_max(s, sub):
    lst = list()
    for i in s:
        lst.append(0)
        
    for i in range(len(s) - len(sub), -1, -1):
        if s[i: i + len(sub)] == sub:
            if i + len(sub) > len(s)-1:
                lst[i] = 1
        
            else:
                lst[i] = lst[i + len(sub)] + 1
    return max(lst)

    
x = open(argv[2])
dna = x.read()

new = list()

for i in four:
    a = get_max(dna, i)
    new.append(str(a))
    

bo = False
for i in st:
    x = i.split(",")
    if x[1:] == new:
        print(x[0])
        bo = True
        
if not bo:
    print("No match")