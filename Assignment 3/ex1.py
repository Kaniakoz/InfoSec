import math
import sys

encrypt = True if input() == "e" else False
p, q, e = map(int, input().split())
n = p * q
if not encrypt:

    def find_lin_comb(num1, num2, target=1):
        mult1 = 0
        mult2 = 0
        curr_target = target
        curr_x = num2

        while curr_x != curr_target:
            if curr_x > curr_target:
                curr_target += num1
                mult1 += 1
            else:
                curr_x += num2
                mult2 += 1

        return mult1, mult2

    def calc_private_key(p, q, e):
        totient_n = (p - 1) * (q - 1)
        target = math.gcd(e, totient_n)
        e_mult, totient_n_mult = find_lin_comb(e, totient_n, target)
        d = (totient_n - e_mult) % totient_n
        return d

    d = calc_private_key(p, q, e)
new_message = input()
while new_message is not None:
    new_message = int(new_message)
    if encrypt:
        print(int(pow(new_message, e) % n))
    else:
        print(int(pow(new_message, d) % n))
    try:
        new_message = input()
    except EOFError:
        new_message = None
