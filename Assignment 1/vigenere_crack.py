import math
import sys
from copy import deepcopy

lower_bound = int(input())
upper_bound = int(input())
ciphertext = text = sys.stdin.read()

alphabet = "abcdefghijklmnopqrstuvwxyz"


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


def determine_shift_letter(cipherletter):
    # shift is always calculated wrt to e because of exercise constraints
    shift = ord(cipherletter) - ord("e")
    return alphabet[shift]


def argmax(array: list[int]):
    best = array[0]
    best_index = 0
    for i in range(len(array)):
        if array[i] > best:
            best = array[i]
            best_index = i
    return best_index


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
        sys.stdout.write(f"The sum of {key_length} std. devs: {stddevs:.2f}\n")
        stddevs = round(stddevs, 2)
        if stddevs > highest_std:
            highest_std = stddevs
            best_key_length = key_length
            best_key_vectors = deepcopy(key_vectors)
    key = ""
    for index in range(best_key_length):
        letter = alphabet[argmax(best_key_vectors[index])]
        key += determine_shift_letter(letter)
    sys.stdout.write("\n")

    return key


result = vigenere_crack(ciphertext, lower_bound, upper_bound)

print("Key guess:")
sys.stdout.write(result)

# The sum of 10 std. devs:
