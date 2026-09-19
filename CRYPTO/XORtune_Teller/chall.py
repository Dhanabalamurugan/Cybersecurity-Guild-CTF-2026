import os
class XORshift:
    def __init__(self,seed: int):
        self.state = seed & 0xFFFFFFFF
    def next(self) -> int:
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x
        return self.state
flag = b'exploiitm{fake_flag}'
seed = int.from_bytes(os.urandom(8))
rng = XORshift(seed)
pad_len = (-len(flag)) % 4
pt = flag + b'\x00' * pad_len
ct = b''
for i in range(0,len(pt),4):
    key = rng.state
    key_bytes = key.to_bytes(4)
    block = pt[i:i+4]
    ct += bytes(a ^ b for a, b in zip(block, key_bytes))
    rng.next()
print("Ciphertext: ",ct)
print("Completely unrelated integers:")
for _ in range(5):
    print(rng.state & 0xFF) 
    rng.next()
