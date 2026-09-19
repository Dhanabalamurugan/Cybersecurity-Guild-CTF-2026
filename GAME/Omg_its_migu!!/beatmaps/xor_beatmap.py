'''def brute_force_xor():
    # Read the raw scrambled bytes from secret.bmap
    with open("secret.bmap", "rb") as f:
        ciphertext = f.read()

    print("--- Searching for the correct XOR key ---")
    
    for key in range(256):
        decrypted_bytes = bytearray(b ^ key for b in ciphertext)
        
        try:
            # Try to turn the numbers back into a readable string
            decrypted_text = decrypted_bytes.decode('utf-8', errors='ignore')
            
            if "exploiitm" in decrypted_text:
                print(f"[+] FOUND KEY: {hex(key)} (Decimal: {key})")
                print(f"[+] FLAG: {decrypted_text}")
                return
        except Exception:
            continue

    print("'exploiitm' not found :( ")

if __name__ == "__main__":
    brute_force_xor()
'''

'''
def solve():
    # 1. Read the 41 bytes of the secret flag file
    with open("secret.bmap", "rb") as f:
        ciphertext = f.read()

    # 2. Known flag prefix format from your screenshot
    known_prefix = "exploiitm{"
    
    print("--- CRACKING SECRET.BMAP ---")
    
    # METHOD A: Vigenere / ASCII Shift check
    # Let's find the repeating pattern of differences
    diffs = [(ord(known_prefix[i]) - ciphertext[i]) % 256 for i in range(len(known_prefix))]
    print(f"[1] Testing ASCII Shift Key Pattern: {diffs}")
    
    # Try to decrypt using the derived shift key pattern
    # We assume the key length is the pattern size
    for key_len in range(1, len(known_prefix) + 1):
        key = diffs[:key_len]
        decrypted = ""
        for i, byte in enumerate(ciphertext):
            shift = key[i % key_len]
            decrypted += chr((byte + shift) % 256)
        if "exploiitm{" in decrypted:
            print(f"\n[+] SUCCESS via ASCII SHIFT!")
            print(f"[+] Flag: {decrypted}\n")
            return

    # METHOD B: Multi-byte Repeating XOR check
    # Let's find the repeating XOR key pattern
    xor_keys = [ciphertext[i] ^ ord(known_prefix[i]) for i in range(len(known_prefix))]
    print(f"[2] Testing Repeating XOR Key Pattern: {[hex(k) for k in xor_keys]}")
    
    for key_len in range(1, len(known_prefix) + 1):
        key = xor_keys[:key_len]
        decrypted = ""
        for i, byte in enumerate(ciphertext):
            k = key[i % key_len]
            decrypted += chr(byte ^ k)
        if "exploiitm{" in decrypted:
            print(f"\n[+] SUCCESS via REPEATING XOR!")
            print(f"[+] Flag: {decrypted}\n")
            return

    print("\n[-] Automated attack missed. Let's dump the raw key streams to look for English words.")
    print("XOR Keystream bytes as chars: ", "".join(chr(k) if 32 <= k <= 126 else '.' for k in xor_keys))

if __name__ == "__main__":
    solve()
'''
#FIX 3
'''
def solve_final():
    with open("secret.bmap", "rb") as f:
        ciphertext = f.read()

    # The file is 41 bytes long. The last character must be '}'
    target_start = "exploiitm{"
    target_end = "}"
    
    print("--- BRUTE FORCING KEY LENGTH ---")
    
    # Try every possible repeating key length
    for key_len in range(1, 41):
        # Derive a trial key based on the first few bytes
        key = [(ord(target_start[i]) - ciphertext[i]) % 256 for i in range(min(key_len, len(target_start)))]
        
        # If the key length is longer than our known prefix, pad it by guessing
        while len(key) < key_len:
            key.append(0) 
            
        # Try to decrypt the entire file with this key length
        decrypted = ""
        for i, byte in enumerate(ciphertext):
            shift = key[i % key_len]
            decrypted += chr((byte + shift) % 256)
            
        # Check if it matches our structure perfectly
        if decrypted.startswith(target_start) and decrypted.endswith(target_end):
            print(f"KEY LENGTH: {key_len}")
            print(f"Flag: {decrypted}")
            return

    # If simple shift key length tuning misses, try repeating XOR key lengths
    for key_len in range(1, 41):
        key = [ciphertext[i] ^ ord(target_start[i]) for i in range(min(key_len, len(target_start)))]
        while len(key) < key_len:
            key.append(0)
        decrypted = ""
        for i, byte in enumerate(ciphertext):
            k = key[i % key_len]
            decrypted += chr(byte ^ k)
        if decrypted.startswith(target_start) and decrypted.endswith(target_end):
            print(f"XOR KEY LENGTH: {key_len}")
            print(f"Flag: {decrypted}")
            return

if __name__ == "__main__":
    solve_final()
'''

#Fix 4

def solve_visual():
    with open("secret.bmap", "rb") as f:
        ciphertext = f.read()

    print("--- BRUTE FORCING ALL 256 SHIFTS ---")
    # Instead of guessing lengths, let's just test every possible single ASCII shift value 
    # to see if the string aligns into "exploiitm{"
    for shift in range(256):
        decrypted = ""
        for byte in ciphertext:
            decrypted += chr((byte + shift) % 256)
        
        # If any part of our flag format appears, grab it!
        if "expl" in decrypted or "exploiitm" in decrypted:
            print(f"[+] FOUND SHIFT VALUE: {shift}")
            print(f"[+] Flag: {decrypted}")
            return

    # If it's a running multi-byte shift, let's print the raw values directly
    print("[-] Single shift missed. Dumping first 15 bytes to inspect math manually:")
    for i in range(min(15, len(ciphertext))):
        print(f"Byte {i}: {hex(ciphertext[i])}")

if __name__ == "__main__":
    solve_visual()
