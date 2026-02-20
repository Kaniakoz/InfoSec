import sys


def read_binary():
    # split at 0xFF, first part is the key, second is the plaintext
    input_data = sys.stdin.buffer.read()
    delimiter_pos = input_data.find(0xFF)

    key = input_data[:delimiter_pos]
    data = input_data[delimiter_pos + 1:]

    return key, data


def rc4(key, data):
    result = bytearray()

    # Key Scheudling Algorithm
    state = [i for i in range(0, 256)]
    j = 0

    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) % 256
        state[i], state[j] = state[j], state[i]

    # PRGA
    i = j = 0

    # protection (from the book)
    for _ in range(256):
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        _ = state[(state[i] + state[j]) % 256]


    for val in data:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        keystream = state[(state[i] + state[j]) % 256]
        result.append(val ^ keystream)

    return bytes(result)


key, data = read_binary()
encrypted = rc4(key, data)
sys.stdout.buffer.write(encrypted)
