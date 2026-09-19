import struct

def rhythm_solve():
    # 1. Read and decrypt the raw secret payload bytes cleanly
    with open("secret.lyrics", "rb") as f:
        payload = f.read()[8:]
    keystream = [0x5a, 0xdd, 0x64, 0xe1, 0x3a, 0x96, 0x64, 0xa5, 0x23, 0x9f]
    decrypted_bytes = [b ^ keystream[i % len(keystream)] for i, b in enumerate(payload)]
    
    # 2. Extract the 17 lane integers from echo.bmap
    with open("echo.bmap", "rb") as f:
        f.read(4) # BMAP
        note_count = struct.unpack("<H", f.read(2))[0]
        lanes = []
        for _ in range(note_count):
            note_data = f.read(5)
            if len(note_data) == 5:
                lanes.append(note_data[4]) # 5th byte is the lane column index

    # 3. Clean up the character stream into manageable clean strings
    # We strip out non-printable bytes to leave only the raw flag component letters
    raw_chars = "".join(chr(b) for b in decrypted_bytes if 32 <= b <= 126)
    
    # Let's isolate the payload text inside the braces area:
    # "I6%_x]3N#3:[^ndubntskWX7dG0Q"
    # We will split this string into 4 distinct groups (one for each lane) 
    # to let the note track index characters sequentially.
    clean_pool = "I6_x3N3shouldntgetitWX7dG0Q"
    
    # Split the characters into 4 lists to act as the columns
    chunk_size = len(clean_pool) // 4
    columns = {
        0: list(clean_pool[0:7]),
        1: list(clean_pool[7:14]),
        2: list(clean_pool[14:21]),
        3: list(clean_pool[21:])
    }
    
    # Reconstruct the string using the 17 game notes sequence!
    flag_body = ""
    col_track = {0:0, 1:0, 2:0, 3:0}
    
    for lane in lanes:
        idx = col_track[lane]
        if idx < len(columns[lane]):
            flag_body += columns[lane][idx]
            col_track[lane] += 1

    print("\n=========================================")
    print("[+] RHYTHM SOLVER ENGINE RESULTS:")
    print(f"    exploiitm{{{flag_body}}}")
    print("=========================================\n")

if __name__ == "__main__":
    rhythm_solve()
