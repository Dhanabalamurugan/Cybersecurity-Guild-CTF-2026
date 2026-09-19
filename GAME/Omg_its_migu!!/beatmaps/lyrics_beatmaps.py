def solve_true_8byte():
    with open("secret.lyrics", "rb") as f:
        payload = f.read()[8:]

    # The exact 8-byte key prefix sequence derived directly from the word "exploiit"
    target = "exploiit"
    key = [payload[i] ^ ord(target[i]) for i in range(8)]
    
    print("--- 8-BYTE ALIGNED STRUCTURAL TEXT ---")
    
    # Decrypt using the precise 8-byte repeating block key
    decrypted = []
    for i, byte in enumerate(payload):
        decrypted.append(chr(byte ^ key[i % 8]))
        
    print("".join(decrypted))

if __name__ == "__main__":
    solve_true_8byte()
