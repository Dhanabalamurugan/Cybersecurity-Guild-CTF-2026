import struct

def parse_and_solve():
    # 1. Read the raw secret payload bytes
    with open("secret.lyrics", "rb") as f:
        data = f.read()
        
    # The first 8 bytes are the LYRC header. Let's isolate the raw content.
    payload = data[8:]
    print(f"--- PARSING CONTAINER METADATA ---")
    print(f"Total payload size to slice: {len(payload)} bytes")

    # The verified 10-byte keystream segment from the front of the flag
    leak_key = [0x5a, 0xdd, 0x64, 0xe1, 0x3a, 0x96, 0x64, 0xa5, 0x23, 0x9f]

    # Let's cleanly print out every byte chunk string separated by non-printable areas
    # to find the exact uncorrupted inside-braces flag segment.
    print("\n--- UNMASKING STRUCTURAL LINE payLOADS ---")
    
    # Try multiple rolling structural index combinations
    for offset in range(4):
        candidate = ""
        for i, byte in enumerate(payload):
            # Apply key transformation accounting for float tracking drifts
            k = leak_key[(i - offset) % len(leak_key)]
            candidate += chr(byte ^ k)
            
        # Extract and print out anything that fits the clean flag pattern format
        import re
        matches = re.findall(r"exploiitm\{[A-Za-z0-9_#$%\^\&\*\-\+\[\]]+?\}", candidate)
        for flag in matches:
            print(f"[+] POTENTIAL STRUCTURAL FLAG MATCH: {flag}")

    # Broad character recovery fallback block
    decrypted_raw = "".join(chr(b ^ leak_key[i % len(leak_key)]) for i, b in enumerate(payload))
    print("\n--- RAW UNFILTERED CHARACTER STREAM ---")
    print("".join(c if (32 <= ord(c) <= 126) else f"\\x{ord(c):02x}" for c in decrypted_raw))

if __name__ == "__main__":
    parse_and_solve()
