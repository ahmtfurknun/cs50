
while True:
    n = input("Change owed: ")
    try:
        n = float(n)
        if not n > 0:
            continue
        else:
            n = float(n) * 100
            break
    except:
        continue
    
quarters = dimes = nickels = pennies = 0

while n != 0:
    if n >= 25:
        quarters += 1
        n -= 25
        
    elif n >= 10:
        dimes += 1
        n -= 10
        
    elif n >= 5:
        nickels += 1
        n -= 5
        
    else:
        pennies += 1
        n -= 1


print(quarters+dimes+nickels+pennies)        