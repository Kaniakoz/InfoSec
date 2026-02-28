def calc_private_key(p, q, e):
    totient_n = (p - 1) * (q - 1)
    d = pow(e, -1, totient_n)
    return d

encrypt = True if input() == "e" else False
p, q, e = map(int, input().split())
n = p * q
if not encrypt:
    d = calc_private_key(p, q, e)
new_message = input()
while new_message is not None:
    new_message = int(new_message)
    if encrypt:
        print(pow(new_message, e, n))
    else:
        print(pow(new_message, d, n))
    try:
        new_message = input()
    except EOFError:
        new_message = None
