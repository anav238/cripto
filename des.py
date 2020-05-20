# Vasiliu Ana - IIA3

import random

import numpy as np

ip = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

inverse_ip = list(range(1, 65))
for index in range(0, 64):
    inverse_ip[ip[index] - 1] = index + 1

pc1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

expansion = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

s = []
with open('s-boxes.txt', 'r') as f:
    s = [[int(num) for num in line.split()] for line in f if line.strip() != ""]

p = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]


def get_binary_array(num, size):
    bin_array = []
    while num != 0:
        bit = num % 2
        bin_array.insert(0, bit)
        num = num // 2
    while len(bin_array) < size:
        bin_array.insert(0, 0)
    return bin_array


def apply_permutation(x, perm):
    y = []
    for i in range(0, len(perm)):
        y.append(x[perm[i] - 1])
    return y


def f(a, j):
    exp_a = apply_permutation(a, expansion)
    b = xor(exp_a, j)
    c = []
    for i in range(0, 8):
        bi = b[(i * 6):(i * 6 + 6)]
        row = bi[5] * 1 + bi[0] * 2
        col = bi[4] * 1 + bi[3] * 2 + bi[2] * 4 + bi[1] * 8
        num = s[i][16 * row + col]
        binary = get_binary_array(num, 4)
        c.extend(binary)
    return apply_permutation(c, p)


def xor(u, v):
    w = []
    for i in range(0, len(u)):
        w.append(u[i] ^ v[i])
    return w


key_schedule = []


def encrypt(x, k):
    x = apply_permutation(x, ip)
    k = apply_permutation(k, pc1)

    c = k[:28]
    d = k[28:]
    c = np.roll(c, -1)
    d = np.roll(d, -1)

    u = x[:32]
    v = x[32:]
    key_schedule.clear()
    for i in range(2, 18):
        k = apply_permutation(np.concatenate([c, d]), pc2)
        key_schedule.append(k)
        old_u = u
        old_v = v
        u = old_v
        v = xor(old_u, f(old_v, k))
        if i in (2, 9, 16):
            c = np.roll(c, -1)
            d = np.roll(d, -1)
        else:
            c = np.roll(c, -2)
            d = np.roll(d, -2)

    x = apply_permutation(np.concatenate([v, u]), inverse_ip)
    return x


def decrypt(y):
    y = apply_permutation(y, ip)
    u = y[:32]
    v = y[32:]

    for i in range(15, -1, -1):
        old_u = u
        old_v = v
        u = old_v
        v = xor(old_u, f(old_v, key_schedule[i]))

    y = apply_permutation(np.concatenate([v, u]), inverse_ip)
    return y


message = np.random.choice([0, 1], 64)
# message = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1,
# 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]

key1 = np.random.choice([0, 1], 64)
# key1 = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0,
# 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1]
key2 = np.random.choice([0, 1], 64)

crypto_text = encrypt(message, key1)
decrypted_text = decrypt(crypto_text)

print(message)
# print(key)
print(crypto_text)
print(decrypted_text)


def attack(plaintext, crypted):
    m1 = dict()
    m2 = dict()
    for i in range(1, 256):
        num = i ^ 8
        k = get_binary_array(num, 64)
        mi = ''.join(map(str, encrypt(plaintext, k)))
        mj = ''.join(map(str, decrypt(crypted)))
        m1[mi] = num
        m2[mj] = num
    possible_keys = []
    for text in m2:
        if text in m1:
            possible_keys.append([m1[text], m2[text]])
    return possible_keys


attack_num_1 = random.randrange(1, 256) ^ 8
attack_num_2 = random.randrange(1, 256) ^ 8
attack_key_1 = get_binary_array(attack_num_1, 64)
attack_key_2 = get_binary_array(attack_num_2, 64)
print("Actual keys: " + str(attack_num_1) + " " + str(attack_num_2))

attack_crypto_text = encrypt(encrypt(message, attack_key_1), attack_key_2)
attack_obtained_keys_1 = attack(message, attack_crypto_text)

if len(attack_obtained_keys_1) > 1:
    message_2 = np.random.choice([0, 1], 64)
    attack_crypto_text_2 = encrypt(encrypt(message_2, attack_key_1), attack_key_2)
    attack_obtained_keys_2 = attack(message_2, attack_crypto_text)
    intersection = list(set(attack_obtained_keys_1) & set(attack_obtained_keys_2))
    print("Keys: " + str(intersection))
else:
    print("Keys: " + str(attack_obtained_keys_1))