import sys


def get_input(encrypt):

    if encrypt:
        public_key = input().split()
    else:
        m, n = map(int, input().split())
        knapsack = input().split()
    input_list = []
    newinput = input()
    while newinput is not None:
        input_list.append(newinput)
        try:
            newinput = input()
        except EOFError:
            newinput = None
    if encrypt:
        return public_key, input_list
    else:
        return m, n, knapsack, input_list


def compute_modular_inverse_m(m, n):
    target = 1
    computed_num = 0
    while computed_num != target:
        target += n
        possible_modular_inverse = target // m
        computed_num = possible_modular_inverse * m
    return possible_modular_inverse


encrypt = True if input() == "e" else False
if encrypt:
    public_key, input_list = get_input(encrypt)
    for integer in input_list:
        integer = int(integer)
        binary_integer = bin(integer)[2:]
        binary_integer_list = [int(num) for num in binary_integer]
        binary_integer_list.reverse()
        for _ in range(len(public_key) - len(binary_integer_list)):
            binary_integer_list.append(0)
        cipher = sum([int(a) * int(b) for a, b in zip(public_key, binary_integer_list)])
        print(cipher)

else:
    m, n, knapsack, input_list = get_input(encrypt)
    m = int(m)
    n = int(n)
    knapsack.reverse()
    modular_inverse = compute_modular_inverse_m(m, n)
    for integer in input_list:
        integer = int(integer)
        s = (integer * modular_inverse) % n
        decrypt_num = ""
        for x in range(len(knapsack)):
            current_num = int(knapsack[x])
            if current_num > s:
                decrypt_num += "0"
            else:
                s -= current_num
                decrypt_num += "1"
        print(int(decrypt_num, 2))
