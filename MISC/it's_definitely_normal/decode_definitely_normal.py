'''import os

# Force the script to look inside its own folder, not the workspace root
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_files = [f for f in os.listdir(script_dir) if f.endswith('.txt')]

if not txt_files:
    print("[-] Error: No .txt transcript file found in this folder!")
    print("[-] Please move the downloaded transcript file here.")
    exit()

filename = os.path.join(script_dir, txt_files[0])
print(f"[+] Reading hidden characters directly from: {filename}")

with open(filename, 'r', encoding='utf-8') as f:
    text = f.read()

binary_data = ""
for char in text:
    if char == '\u200b':    # Zero-Width Space
        binary_data += '0'
    elif char == '\u200c':  # Zero-Width Non-Joiner
        binary_data += '1'
    elif char == '\u200d':  # Zero-Width Joiner
        binary_data += '1'  # Try 1 if they used it as a marker

# Convert binary string to ASCII text
flag = ""
for i in range(0, len(binary_data), 8):
    byte = binary_data[i:i+8]
    if len(byte) == 8:
        flag += chr(int(byte, 2))

print(f"[+] Hidden Message Found: {flag}")


import unicodedata

with open("transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

hidden = [
    c for c in text
    if unicodedata.category(c) == "Cf"
]

print("Count:", len(hidden))
print("Characters:")
for c in hidden:
    print(f"U+{ord(c):04X}", unicodedata.name(c, "UNKNOWN"))''

#To find which words are modified
import unicodedata

with open("transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

for i, c in enumerate(text):
    if c == "\u200b":
        print(i, repr(text[max(0, i-15):i+15]))

bits = ""

for word in text.split():
    bits += "1" if "\u200b" in word else "0"

# Try every possible offset/grouping
for offset in range(8):
    b = bits[offset:]
    data = []

    for i in range(0, len(b) - 7, 8):
        data.append(chr(int(b[i:i+8], 2)))

    result = ''.join(data)

    if any(x in result.lower() for x in ["flag", "exploiitm", "{", "ctf"]):
        print(offset, repr(result))'''

text = open("transcript.txt", encoding="utf-8").read()

positions = [i for i,c in enumerate(text) if c == "\u200b"]

for p in positions:
    print(p, repr(text[p-1]), repr(text[p+1]))