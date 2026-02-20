import sys


def read_binary():
    # split at 0xFF, first part is the key, second is the plaintext
    input_data = sys.stdin.buffer.read()
    delimiter_pos = input_data.find(0xFF)

    key = input_data[:delimiter_pos]
    data = input_data[delimiter_pos + 1:]

    return key, data


def vernam_cipher(key, data):
    # XOR key and plaintext
    result = bytearray()
    for i in range(len(data)):
        result.append(key[i] ^ data[i])

    return bytes(result)


key, data = read_binary()
encrypted = vernam_cipher(key, data)
sys.stdout.buffer.write(encrypted)
