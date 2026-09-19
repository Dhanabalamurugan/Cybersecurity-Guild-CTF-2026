import struct

def restore():
    header = b"BMAP"
    note_count = struct.pack("<H", 17)
    
    # The original raw binary byte sequence from your xxd echo.bmap trace
    raw_payload = bytes.fromhex(
        "11003227973f01467cd93f00219fc840030ae6ea400075522c4101"
        "75522c4102308d364100308d36410354a358410254a3584103ec12"
        "824100ec12824102de08c94103b614e64101b614e64102bc5b0942"
        "00bc5b094203"
    )
    
    with open("beatmaps/echo.bmap", "wb") as f:
        f.write(header + raw_payload)
    print("[+] echo.bmap restored to original 17-note game state.")

if __name__ == "__main__":
    restore()
