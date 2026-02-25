import sys


def read_binary():
    input_data = sys.stdin.buffer.read()
    first_delimiter_pos = input_data.find(0xFF)

    encrypt = input_data[:first_delimiter_pos]
    key_text_data = input_data[first_delimiter_pos + 1 :]
    second_delimiter_pos = key_text_data.find(0xFF)
    key = key_text_data[:second_delimiter_pos]
    text = key_text_data[second_delimiter_pos + 1 :]

    return encrypt, key, text


def round_function(key):
    return key


def feistel_8block(key, text, encrypt) -> bytearray:
    key = bytearray(key)
    text = bytearray(text)
    lh, rh = text[0:4], text[4:]

    rf_result = round_function(key)
    if encrypt:
        lh = bytearray(a ^ b for (a, b) in zip(lh, rf_result))
        rh = bytearray(rh)
        lh, rh = rh, lh

    else:
        rh = bytearray(a ^ b for (a, b) in zip(rh, rf_result))
        lh = bytearray(lh)
        lh, rh = rh, lh

    return lh + rh


def feistel_cipher(encrypt, key, text, rounds):
    encrypt = True if encrypt.decode() == "e" else False
    text = bytearray(text)
    key = bytearray(key)
    rounds = len(key) // 4
    converttext = bytearray()
    if encrypt:
        for x in range(0, (len(text) // 8)):
            current_text = text[x * 8 : (x + 1) * 8]
            for x in range(rounds):
                current_key = key[x * 4 : (x + 1) * 4]
                current_text = bytearray(
                    feistel_8block(current_key, current_text, encrypt)
                )
            converttext.extend(current_text)

    else:
        for x in range(0, (len(text) // 8)):
            current_text = text[x * 8 : (x + 1) * 8]
            for x in range(0, -rounds, -1):
                current_key = key[len(key) + 4 * (x - 1) : len(key) + 4 * x]
                current_text = bytearray(
                    feistel_8block(current_key, current_text, encrypt)
                )
            converttext.extend(current_text)
    return bytes(converttext)


encrypt, key, text = read_binary()
output = feistel_cipher(encrypt, key, text, 2)
sys.stdout.buffer.write(output)
