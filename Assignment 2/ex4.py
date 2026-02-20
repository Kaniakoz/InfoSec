import math

def is_public_valid(public_key, private_key, n, m) -> bool:
    proper_public = []
    for i in private_key:
        proper_public.append((i * m) % n)
    #print(proper_public)
    #print(public_key)
    return True if public_key == proper_public else False


def is_private_valid(private) -> bool:
    # just checking if it is a superincreasing knapsack?
    for i in range(1, len(private)):
        if private[i] <= sum(private[:i]):
            return False
    if n <= sum(private):
        return False
    if math.gcd(m, n) != 1:
        return False
    return True


def outputting(priv, pub):
    if priv and pub:
        print(1)
    elif priv and not pub:
        print(0)
    else:
        print(-1)


m, n = map(int, input().split())
# 41 491

private_key = list(map(int, input().split()))
public_key = list(map(int, input().split()))


priv_valid = is_private_valid(private_key)
if priv_valid:
    pub_valid = is_public_valid(public_key, private_key, n, m)
else:
    pub_valid = False
outputting(priv_valid, pub_valid)

