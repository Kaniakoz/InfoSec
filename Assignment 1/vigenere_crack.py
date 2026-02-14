import math
import sys
from copy import deepcopy

lower_bound = int(input())
upper_bound = int(input())
ciphertext = text = sys.stdin.read()


def match_character_to_index(character):
    if ord(character.lower()) - ord("a") > 25 or ord(character.lower()) - ord("a") < 0:
        return 26
    return ord(character.lower()) - ord("a")


def square_vector(vector: list[int]):
    vectorcopy = deepcopy(vector)
    vectorcopy = [element**2 for element in vectorcopy]
    return vectorcopy


def std_vector(vector: list[int]):
    return math.sqrt((sum(square_vector(vector)) / 26) - (sum(vector) / 26) ** 2)


def vigenere_crack(ciphertext, lower_bound, upper_bound):
    highest_std, best_key_length = 0, 0
    for key_length in range(lower_bound, upper_bound + 1):
        key_vectors = [[0] * 26 for _ in range(key_length)]
        key_index = 0
        # parse cipher text
        for character in ciphertext:
            if (
                ord(character.lower()) - ord("a") > 25
                or ord(character.lower()) - ord("a") < 0
            ):
                pass
            else:
                key_vectors[key_index][ord(character.lower()) - ord("a")] += 1
                key_index += 1
            if key_length == key_index:
                key_index = 0
        stddevs = 0
        for vector in key_vectors:
            stddevs += std_vector(vector)
        stddevs = round(stddevs, 2)
        sys.stdout.write(f"sum of {key_length} std. devs: {stddevs}\n")
        if stddevs > highest_std:
            highest_std = stddevs
            best_key_length = key_length
    sys.stdout.write(f"key length guess: {best_key_length}\n")
    sys.stdout.write("\n")
    # key guess part


result = vigenere_crack(ciphertext, lower_bound, upper_bound)

print("Key guess:")
sys.stdout.write(result)

# The sum of 10 std. devs:
