# Vasiliu Ana - IIA3

import random;


def init(k):
    l = len(k)
    j = 0
    s0 = []
    for i in range(0, 256):
        s0.append(i)
    for i in range(0, 256):
        j = (j + s0[i] + k[i % l]) % 256
        s0[i], s0[j] = s0[j], s0[i]
    return 0, 0, s0


def trans(i, j, s):
    i = i + 1
    j = (j + s[i]) % 256
    s[i], s[j] = s[j], s[i]
    return i, j, s, s[(s[i] + s[j]) % 256]


def generate_keystream(k, n):
    i, j, s = init(k)
    keystream = []
    for i in range(1, n + 1):
        i, j, s, b = trans(i, j, s)
        keystream.append(b)
    return keystream


k = [0, 1, 2, 3, 4, 5]
keystream = generate_keystream(k, len(k))


def encrypt(m):
    c = []
    for i in range(0, len(m)):
        c.append(m[i] ^ keystream[i])
    return c


def decrypt(c):
    m = []
    for i in range(0, len(c)):
        m.append(c[i] ^ keystream[i])
    return m


m = [250, 122, 0, 10, 50, 250]
c = encrypt(m)
print(c)
d = decrypt(c)
print(d)


def checkKeystreamBias():
    tests_to_do = pow(2, 16)
    l = 16
    n_zero = []
    for i in range(0, l):
        n_zero.append(0)
    for test in range(0, tests_to_do):
        k = []
        for i in range(0, l):
            k.append(random.randint(0, 255))
        keystream = generate_keystream(k, l)
        for i in range(1, l):
            if keystream[i] == 0:
                n_zero[i] += 1
    print("Probabilitatea ca al doilea byte sa fie 0: ")
    print(n_zero[1] / tests_to_do)
    print("Probabilitatea asteptata ca al doilea byte sa fie 0: ")
    print(1 / 128)
    print("Probabilitatea asteptata ca byte-ul r, cu r>=3 sa fie 0: " + str(1 / 256 + 1 / pow(2, 16)))
    for i in range(2, l):
        print("Probabilitatea ca byte-ul " + str(i + 1) + " sa aiba valoarea 0 este " + str(n_zero[i] / tests_to_do))


checkKeystreamBias()
