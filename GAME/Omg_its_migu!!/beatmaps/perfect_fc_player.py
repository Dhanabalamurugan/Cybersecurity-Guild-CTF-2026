import struct

def simulate_perfect_play():
    # 1. Read and decrypt the raw characters cleanly from secret.lyrics
    with open("secret.lyrics", "rb") as f:
        payload = f.read()[8:]
    keystream = [0x5a, 0xdd, 0x64, 0xe1, 0x3a, 0x96, 0x64, 0xa5, 0x23, 0x9f]
    decrypted_bytes = [b ^ keystream[i % len(keystream)] for i, b in enumerate(payload)]
    raw_chars = "".join(chr(b) for b in decrypted_bytes if 32 <= b <= 126)
    
    # Isolate only the true data block inside the flag bounds
    start_idx = raw_chars.find("exploiitm{") + len("exploiitm{")
    end_idx = raw_chars.find("}", start_idx)
    clean_pool = raw_chars[start_idx:end_idx].replace("?", "")

    # 2. Read the timestamps and lanes from echo.bmap to sort them chronologically
    notes = []
    with open("echo.bmap", "rb") as f:
        f.read(4) # Skip BMAP header
        note_count = struct.unpack("<H", f.read(2))[0]
        
        for _ in range(note_count):
            note_bytes = f.read(5)
            if len(note_bytes) == 5:
                # The first 4 bytes are a little-endian float timestamp
                timestamp = struct.unpack("<f", note_bytes[:4])[0]
                # The 5th byte is the lane index (0, 1, 2, or 3)
                lane = note_bytes[4]
                notes.append((timestamp, lane))

    # Sort the game notes strictly by their execution time (chronological play order)
    notes.sort(key=lambda x: x[0])
    sorted_lanes = [n[1] for n in notes]
    
    print("--- 100% ACCURACY CHART SEQUENCING ---")
    print(f"Chronological Lane Hits: {sorted_lanes}")
    print(f"Total Text Character Pool Size: {len(clean_pool)}")

    # 3. Reconstruct the string matrix using the sorted lane inputs
    chunk_size = len(clean_pool) // 4
    lanes_data = {
        0: clean_pool[0:chunk_size],
        1: clean_pool[chunk_size:chunk_size*2],
        2: clean_pool[chunk_size*2:chunk_size*3],
        3: clean_pool[chunk_size*3:]
    }

    flag_body = ""
    counters = {0: 0, 1: 0, 2: 0, 3: 0}
    
    for l in sorted_lanes:
        if counters[l] < len(lanes_data[l]):
            flag_body += lanes_data[l][counters[l]]
            counters[l] += 1

    print("\n=========================================")
    print("[+] FULL COMBO FLAG OUTPUT:")
    print(f"    exploiitm{{{flag_body}}}")
    print("=========================================\n")

if __name__ == "__main__":
    simulate_perfect_play()
