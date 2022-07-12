while True:
    n = input("Height: ")
    if n.isnumeric() and 1 <= int(n) <= 8:
        n = int(n)
        break
        
for i in range(1, n+1):
    print((n-i) * " " + i * "#")