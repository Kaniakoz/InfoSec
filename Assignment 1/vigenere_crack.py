import sys

lower_bound = int(input())
upper_bound = int(input())
ciphertext = text = sys.stdin.read()

def vigenere_crack(ciphertext, lower_bound, upper_bound):
    for key_length in range(lower_bound, upper_bound + 1):
        pass

result = vigenere_crack(ciphertext, lower_bound, upper_bound)

print("Key guess:")
sys.stdout.write(result)

# The sum of 10 std. devs: