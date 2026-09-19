import struct

def build_hack_map():
    header = b"BMAP"
    note_count = struct.pack("<H", 1)
    
    timestamp = struct.pack("<f", 1.0)
    lane = struct.pack("B", 0)
    
    with open("beatmaps/echo.bmap", "wb") as f:
        f.write(header + note_count + timestamp + lane)
        
    print("[+] Hacked beatmap written successfully!")

if __name__ == "__main__":
    build_hack_map()
