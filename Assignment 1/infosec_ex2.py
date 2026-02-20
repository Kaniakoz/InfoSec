import sys

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = lowercase + uppercase

def shift_endecrypt(e: bool, shift: int):
    shift %= 26
    if not e:
        shift = -shift
    shifted = lowercase[shift:] + lowercase[:shift] + uppercase[shift:] + uppercase[:shift]
    return str.maketrans(alphabet, shifted)


def map_endecrypt(e: bool, mapping: str):
    mapping = mapping + mapping.upper()
    if e:
        return str.maketrans(alphabet, mapping)
    else:
        return str.maketrans(mapping, alphabet)


# if this isn't fast enough, I'm switching to cpp

instruction = list(input().split(" "))
text = sys.stdin.read()

it = iter(instruction)

full_translation = {i:i for i in range(256)}

for op, arg in zip(it, it):
    if arg.isnumeric():
        arg = int(arg)
        translation = shift_endecrypt(op == 'e', arg)
    else:
        translation = map_endecrypt(op == 'e', arg)
    full_translation = {k: translation.get(v, v) for k, v in full_translation.items()}

text = text.translate(full_translation)

sys.stdout.write(text)