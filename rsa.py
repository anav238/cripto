from Cryptodome.Util import number
import time
import math
import random


def euclid_extins(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = euclid_extins(b % a, a)
        return g, x - (b // a) * y, y


def power_modulo(a, b, n):
    result = 1
    for i in range(0, b):
        result = (result * a) % n
    return result


def rsa_crt_dec(d, p, q, c):
    dp = d % (p - 1)
    dq = d % (q - 1)
    g, x, y = euclid_extins(q, p)
    q_inv = x % p
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    h = (q_inv * (m1 - m2)) % p
    m = (m2 + h * q) % (p * q)
    return m2


def rsa(m):
    p, q = 0, 0
    while not (q < p < 2 * q):
        p = number.getPrime(514)
        q = number.getPrime(514)
    n = p * q
    e = 65537
    v_phi = (p - 1) * (q - 1)
    g, x, y = euclid_extins(e, v_phi)
    d = x % v_phi

    c = pow(m, e, n)

    start_time = time.time()
    dec = pow(c, d, n)
    elapsed_time = time.time() - start_time

    print("Mesaj: " + str(m))
    print("Mesaj criptat: " + str(c))
    print("Mesaj decriptat: " + str(dec))

    print("Timp de executie pentru decriptarea obisnuita: ")
    print("%s secunde" % elapsed_time)

    start_time = time.time()
    dec_crt = rsa_crt_dec(d, p, q, c)
    elapsed_time = time.time() - start_time
    print("\nMesaj decriptat cu CRT: " + str(dec_crt))

    print("Timp de executie pentru decriptarea cu TCR: ")
    print("%s secunde" % elapsed_time)

    d = n
    while math.gcd(d, v_phi) != 1 or 81 * (d ** 4) >= n:
        d = number.getRandomNBitInteger(32)
    g, x, y = euclid_extins(d, v_phi)
    e = x % v_phi
    print("Actual p and q: " + str(p) + " " + str(q))
    print("Actual d: " + str(d))
    wiener_attack(n, e)


def sqrt_large_num(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def criteriu(l, d, n, e):
    if l == 0:
        return 0
    if (e * d - 1) % l != 0:
        return 0
    s = n - (e * d - 1) // l + 1
    rez = s * s - 4 * n
    sqrt = sqrt_large_num(rez)
    if rez >= 0 and sqrt * sqrt == rez and (s + sqrt) % 2 == 0:
        print("Found p and q: " + str((s + sqrt) // 2) + " " + str((s - sqrt) // 2))
        return 1
    return 0


def wiener_attack(n, e):
    i = 0
    while True:
        i = i + 1
        if i == 1:
            alpha1, beta1, r1 = e // n, 1, e % n
            l, d = alpha1, beta1
        elif i == 2:
            alpha2, beta2, r2 = alpha1 * (n // r1) + 1, n // r1, n % r1
            l, d = alpha2, beta2
        else:
            if r2 == 0:
                print("oops")
                break
            q = r1 // r2
            rez = r1 % r2
            r1 = r2
            r2 = rez
            alpha, beta = q * alpha2 + alpha1, q * beta2 + beta1
            alpha1, beta1 = alpha2, beta2
            alpha2, beta2 = alpha, beta
            l, d = alpha, beta
        if criteriu(l, d, n, e) == 1:
            break
    print("d found: " + str(d))

rsa(123)
