def input_process():
    x, y = input().split(",")
    x = int(x[1:])
    y = int(y[:-1])
    a, b, p = map(int, input().split())
    m, n = map(int, input().split())
    return x, y, a, b, p, m, n


def point_mul(k, x, y, a, p):
    result = (None, None)
    add = (x, y)
    # this double and add algorithm from wikipedia

    while k > 0:
        if k & 1:
            result = point_add(result[0], result[1],
                               add[0], add[1], a, p)

        add = point_add(add[0], add[1], add[0], add[1], a, p)

        k >>= 1

    return result


def point_add(x1, y1, x2, y2, a, p):
    if x1 is None:
        return x2, y2
    if x2 is None:
        return x1, y1

    if x1 == x2 and (y1 + y2) % p == 0:
        return None, None

    if x1 == x2 and y1 == y2:
        lambd = ((3 * x1 ** 2 + a) * pow(2*y1, -1, p)) % p
    else:
        lambd = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    new_x = (lambd ** 2 - x1 - x2) % p
    new_y = (lambd*(x1-new_x) - y1) % p
    return new_x, new_y


x, y, a, b, p, m, n = input_process()

# apx, apy = point_mul(m, x, y, a, p)
bpx, bpy = point_mul(n, x, y, a, p)
fin_x, fin_y = point_mul(m, bpx, bpy, a, p)

print(f"({fin_x}, {fin_y})")

