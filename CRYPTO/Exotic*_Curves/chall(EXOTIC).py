import random, os
from hashlib import sha1, sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from collections import namedtuple

with(open('flag.txt') as f):
    flag = f.read().encode('utf-8')

Point = namedtuple("Point", "x y")

p = 106267532015697168520337191172088148412515620576161290874946589402878151571249
D = 42233242539448005099475028269993990446352013294366498148311505626717263001612
G = Point(x=102048330668061011078177084521527399007542737797660957136363503399801919446230, y=73159115351277642048716110709055707500362539496317081461959122153668971225415)
def point_addition(P, Q):
    Rx = (P.x * Q.x + D * P.y * Q.y) % p
    Ry = (P.x * Q.y + P.y * Q.x) % p
    return Point(Rx, Ry)
 
 
def scalar_mul(P, n):
    Q = Point(1, 0)
    while n > 0:
        if n %2 == 1:
            Q = point_addition(Q, P)
        P = point_addition(P, P)
        n = n // 2
    return Q

def gen_keypair():
    d = random.randint(2,p-1)
    return scalar_mul(G,d),d

def gen_shared_secret(P,d):
    return scalar_mul(P,d).x

A, n_a = gen_keypair()
B, n_b = gen_keypair()

shared_sec = gen_shared_secret(A,n_b)
key = sha1(str(shared_sec).encode()).digest()[:16]
iv = os.urandom(16)
flag_enc = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(flag, 16))

print('p : ', p)
print('D : ', D)
print('Alice\'s Public Key : ', A)
print('Bob\'s Public Key: ', B)
print('IV : ', iv.hex())
print('Encrpyted Flag : ', flag_enc.hex())