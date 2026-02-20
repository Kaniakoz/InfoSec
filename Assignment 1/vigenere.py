import sys

def vigenere_encode(text: str, code: str):
    code = code.lower()
    message = []
    key_index = 0
    key_len = len(code)

    for curr in text:
        if curr.isalpha():
            shift = ord(code[key_index % key_len]) - ord('a')

            if curr.isupper():
                curr = chr((ord(curr) - ord('A') + shift) % 26 + ord('A'))
            else:
                curr = chr((ord(curr) - ord('a') + shift) % 26 + ord('a'))

            key_index += 1

        message.append(curr)

    return ''.join(message)


def vigenere_decode(text: str, code: str):
    code = code.lower()
    message = []
    key_index = 0
    key_len = len(code)

    for curr in text:
        if curr.isalpha():
            shift = ord(code[key_index % key_len]) - ord('a')

            if curr.isupper():
                curr = chr((ord(curr) - ord('A') - shift) % 26 + ord('A'))
            else:
                curr = chr((ord(curr) - ord('a') - shift) % 26 + ord('a'))

            key_index += 1

        message.append(curr)
    return ''.join(message)


instruction, code = input().split(" ")
text = sys.stdin.read()

result = vigenere_encode(text, code) if instruction == "e" else vigenere_decode(text, code)

sys.stdout.write(result)