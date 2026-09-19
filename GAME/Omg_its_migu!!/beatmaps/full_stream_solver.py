import struct

def stream_solve():
    with open("secret.lyrics", "rb") as f:
        payload = f.read()[8:]
    keystream = [0x5a, 0xdd, 0x64, 0xe1, 0x3a, 0x96, 0x64, 0xa5, 0x23, 0x9f]
    decrypted_bytes = [b ^ keystream[i % len(keystream)] for i, b in enumerate(payload)]
    
    # Extract ALL valid, clean characters inside the flag zone
    raw_chars = "".join(chr(b) for b in decrypted_bytes if 32 <= b <= 126)
    
    # Isolate everything after the opening brace
    start_idx = raw_chars.find("exploiitm{") + len("exploiitm{")
    body_pool = raw_chars[start_idx:].replace("}", "").replace("?", "")
    
    # The 17 absolute lane column triggers from echo.bmap
    lanes = [1, 0, 3, 0, 1, 2, 0, 3, 2, 3, 0, 2, 3, 1, 2, 0, 3]
    
    print(f"--- Full Body Pool Characters: {body_pool} ---")
    
    # Let's index characters directly using the note lanes as absolute multipliers
    flag_body = ""
    for i, lane in enumerate(lanes):
        # Calculate a rolling jump based on the lane index position
        idx = (i * 2 + lane) % len(body_pool)
        flag_body += body_pool[idx]

    print("\n=========================================")
    print("[+] FULL DYNAMIC STREAM FLAG RESULTS:")
    print(f"    exploiitm{{{flag_body}}}")
    print("=========================================\n")

if __name__ == "__main__":
    stream_solve()
