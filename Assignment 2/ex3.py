import sys


def read_binary():
    # split at 0xFF, first part is the key, second is the plaintext
    input_data = sys.stdin.buffer.read()
    first_delimiter_pos = input_data.find(0xFF)

    encrypt = input_data[:first_delimiter_pos]
    key_text_data = input_data[first_delimiter_pos + 1 :]
    second_delimiter_pos = key_text_data.find(0xFF)
    key = key_text_data[:second_delimiter_pos]
    text = key_text_data[second_delimiter_pos + 1 :]

    return encrypt, key, text


def feistel_8block(key, text, encrypt=True) -> bytearray:
    key = bytearray(key)
    text = bytearray(text)
    # k1 = key[0:4]
    # k2 = key[4:8]
    lh, rh = text[0:4], text[4:]

    if encrypt:
        lh = bytearray(a ^ b for (a, b) in zip(key, lh))
        rh = bytearray(rh)
        lh, rh = rh, lh

        lh = bytearray(a ^ b for (a, b) in zip(key, lh))
        lh, rh = rh, lh

    else:
        lh = bytearray(lh)
        rh = bytearray(a ^ b for (a, b) in zip(key, rh))
        lh, rh = rh, lh

        lh = bytearray(lh)
        rh = bytearray(a ^ b for (a, b) in zip(key, rh))
        lh, rh = rh, lh

    return lh.join([rh])


def feistel_cipher(encrypt, key, text):
    encrypt = True if encrypt.decode() == "e" else False
    text = bytearray(text)
    key = bytearray(key)
    converttext = bytearray()
    sys.stdout.write(f"len key : {len(key)} len text: {len(text)} \n")
    for x in range(0, (len(text) // 8)):
        current_key = key[x * 4 : (x + 1) * 4]
        k1 = current_key[0:4]
        k2 = current_key[4:8]
        current_text = text[x * 8 : (x + 1) * 8]
        # current_text = bytearray(current_text)
        once_encrypted = bytearray(feistel_8block(current_key, current_text, encrypt))
        # twice_encrypted = bytearray(feistel_8block(k2, once_encrypted, not encrypt))
        # thrice_encrypted = feistel_8block(k1, twice_encrypted, encrypt)
        converttext.extend(once_encrypted)

        # sys.stdout.write(converttext.decode())

    return bytes(converttext)


encrypt, key, text = read_binary()
output = feistel_cipher(encrypt, key, text)
# sys.stdout.write(f"str output:{feistel_cipher(encrypt, key, text).decode()}")
sys.stdout.buffer.write(output)
