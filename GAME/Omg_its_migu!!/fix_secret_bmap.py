def decrypt_bmap():
    # Read the scrambled secret map data
    with open("beatmaps/secret.bmap", "rb") as f:
        ciphertext = f.read()

    # The exact 4-byte master key derived from 'n2q~' ^ 'BMAP'
    key = [ord('n') ^ ord('B'), ord('2') ^ ord('M'), ord('q') ^ ord('A'), ord('~') ^ ord('P')]
    print(f"[+] Master 4-Byte Key Found: {[hex(b) for b in key]}")

    # Decrypt every byte of the file using the repeating 4-byte key loop
    decrypted_bytes = bytearray(byte ^ key[i % 4] for i, byte in enumerate(ciphertext))

    # Overwrite secret.bmap with the functional, uncorrupted binary data
    with open("beatmaps/secret.bmap", "wb") as f:
        f.write(decrypted_bytes)
        
    print("[+] secret.bmap has been successfully decrypted and repaired!")

if __name__ == "__main__":
    decrypt_bmap()
