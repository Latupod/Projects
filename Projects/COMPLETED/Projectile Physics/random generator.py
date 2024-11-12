import time

def randgen(seed,n,current):
    if n>0:
        n -= 1
        if current%2 == 0:
            current = ((4*current+1))
        elif current%2 != 0:
            current = ((4*current))
        randgen(n,seed,current)
    return current

def my_rand():
    n = 1
    seed = int(str(int(time.time()*(10**7)))[10:-1])
    print(seed)
    current = seed
    return str(int(randgen(seed,n,current)%6)+1)
    


while True:
    input()
    print(my_rand())