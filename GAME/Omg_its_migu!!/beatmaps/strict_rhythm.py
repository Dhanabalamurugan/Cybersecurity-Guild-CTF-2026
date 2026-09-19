import struct

def pure_solve():
    # 1. Read and decrypt the exact raw string from the container
    with open("secret.lyrics", "rb") as f:
        payload = f.read()[8:]
    keystream = [0x5a, 0xdd, 0x64, 0xe1, 0x3a, 0x96, 0x64, 0xa5, 0x23, 0x9f]
    decrypted = "".join(chr(b ^ keystream[i % len(keystream)]) for i, b in enumerate(payload))
    
    # Extract only the exact characters inside the braces payload area
    start_idx = decrypted.find("exploiitm{") + len("exploiitm{")
    end_idx = decrypted.find("}", start_idx)
    raw_body = decrypted[start_idx:end_idx]
    
    # Strip out the question marks (hidden non-printable bytes) to get the true text array
    clean_body = raw_body.replace("?", "")
    print(f"--- Pure Raw Body Array: {clean_body} (Length: {len(clean_body)}) ---")

    # 2. Define the exact 17 note lane tracks from echo.bmap
    lanes = [1, 0, 3, 0, 1, 2, 0, 3, 2, 3, 0, 2, 3, 1, 2, 0, 3]

    # 3. Split the raw body evenly across the 4 game lanes
    chunk_size = len(clean_body) // 4
    columns = {
        0: list(clean_body[0:chunk_size]),
        1: list(clean_body[chunk_size:chunk_size*2]),
        2: list(clean_body[chunk_size*2:chunk_size*3]),
        3: list(clean_body[chunk_size*3:])
    }
    
    # 4. Play the game notes to extract the true characters sequentially
    flag_body = ""
    col_track = {0:0, 1:0, 2:0, 3:0}
    
    for lane in lanes:
        if col_track[lane] < len(columns[lane]):
            flag_body += columns[lane][col_track[lane]]
            col_track[lane] += 1

    print("\n=========================================")
    print("[+] MATHEMATICALLY CORRECT FLAG:")
    print(f"    exploiitm{{{flag_body}}}")
    print("=========================================\n")

if __name__ == "__main__":
    pure_solve()
