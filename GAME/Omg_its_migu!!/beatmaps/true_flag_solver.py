def print_array_chars():
    with open("secret.lyrics", "rb") as f:
        payload = f.read()[8:]

    keystream = [0x5a, 0xdd, 0x64, 0xe1, 0x3a, 0x96, 0x64, 0xa5, 0x23, 0x9f]
    decrypted_raw = [b ^ keystream[i % len(keystream)] for i, b in enumerate(payload)]
    text_chars = "".join(chr(b) for b in decrypted_raw if 32 <= b <= 126)
    
    print("--- RAW 75-CHARACTER DECRYPTED STREAM ---")
    print(text_chars)
    print("------------------------------------------")

if __name__ == "__main__":
    print_array_chars()
