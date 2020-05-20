import random
import string


def left_rotate(n, d):
    return ((n << d) | (n >> (32 - d))) & 0xffffffff


def sha1(m, t):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    ml = len(m) * 8

    m = ''.join(f'{ord(i):08b}' for i in m)
    m += '1'
    while (len(m) + 1) % 512 != 448:
        m += '0'
    m += bin(ml)[2:].zfill(64)
    # print(hex(int(m, 2)))

    for i in range(0, len(m), 512):
        chunk = m[i:i + 512]
        w = []
        for j in range(0, 512, 32):
            w.append(int(chunk[j:j + 32], 2))
            # print(hex(w[len(w) - 1]))

        for j in range(16, 80):
            w.append(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16])
            w[j] = left_rotate(w[j], 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f, k = 0, 0
        for j in range(0, 80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= j <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + w[j]) & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
            # print(str(j) + "-> A: " + str(hex(a)) + " B: " + str(hex(b)) + " C: " + str(hex(c)) + " D: " + str(hex(d)) + " E: " + str(hex(e)))

        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    if t == 1:
        return hex(hh)
    return hex(h0)


def hamming_distance(a, b):
    a = str(a)
    b = str(b)
    if len(a) != len(b):
        return -1
    dist = 0
    for i in range(0, len(a)):
        if a[i] != b[i]:
            dist += 1
    return dist


def birthday_attack():
    while True:
        found = dict()
        alphabet = string.ascii_letters + string.digits
        for i in range(pow(2, 16)):
            random_length = random.randint(50, 250)
            message = ''.join(random.choice(alphabet) for i in range(random_length))
            hashed = sha1(message, 2)
            if hashed in found:
                print("Common hash: " + str(hashed))
                return message, found[hashed]
            else:
                found[hashed] = message


print(sha1("abc", 1))

print("Experiment efect avalansa")
output1 = sha1("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 1)
print(output1)
output2 = sha1("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopr", 1)
print(output2)
print("Distanta Hamming intre cele 2 este egala cu " + str(hamming_distance(output1, output2)))

print(birthday_attack())

