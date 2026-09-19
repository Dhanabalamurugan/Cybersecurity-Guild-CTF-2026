#### Yummy fruit ####

So download the ss 
try the given flag ,get betrayed.
saw minecraft .
thought of legendary technoblade.
8th std in the qn , now prolly the qn was made by seniors (3rd -4th), so 5-6 yrs before....
youtube video .....but season and episode ? could be a series type shit ...who knows .

Google lens : The selected region showcases a famous Minecraft optical illusion structure built entirely out of diamond blocks, which is commonly featured across viral social media platforms like YouTube and TikTok.

Gemini helped with minecraft series kinda creators : said skeppy (technoblade's frd)
checkout random minecraft ytbers.
went to OSINT him...
these niggers have 100s of videos....

Google suggested Tineye website : ...
TinEye searched over 85.7 billion images but didn't find any matches for your search image.

time goes .....
no idea.....

maybe i need minecraft ball knowledge ?
feels like a detective :)

some red color skin
YouTubers use a very specific, iconic skin that they never change.
Title says Yummy Fruit ??   
has some diamond staircase ,
subtitle says 'pretty much,but today i' : could be in the beginning of the videeo..

SmartPie
wasted a good amt of time , went OSINT again,

searched "yummy fruit minecraft" and literally a video with same name was there . Finally ..... i couldnt find the ss though.


learned something abt google hacking/google dork commands


#### pwn


1.Got  a name ?


[jeeva@archlinux GuildCTF]$ file chal
chal: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=dd25ba0ec249c1d9b2637bcdf6d32884c269dc5d, for GNU/Linux 3.2.0, not stripped
[jeeva@archlinux GuildCTF]$ strings chal
/lib64/ld-linux-x86-64.so.2
fgets
__libc_start_main
setvbuf
stdout
puts
system
stdin
__stack_chk_fail
printf
libc.so.6
GLIBC_2.4
GLIBC_2.2.5
GLIBC_2.34
__gmon_start__
PTE1
/bin/sh
What is your name?
Hello 
Retype name for confirmation
:*3$"
GCC: (Ubuntu 11.4.0-1ubuntu1~22.04.3) 11.4.0
crt1.o
__abi_tag
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
chal.c
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_start_main@GLIBC_2.34
stdout@GLIBC_2.2.5
puts@GLIBC_2.2.5
stdin@GLIBC_2.2.5
_edata
_fini
__stack_chk_fail@GLIBC_2.4
system@GLIBC_2.2.5
printf@GLIBC_2.2.5
gadget
fgets@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
_end
_dl_relocate_static_pie
__bss_start
main
setvbuf@GLIBC_2.2.5
__TMC_END__
_init
.symtab
.strtab
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.sec
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got
.got.plt
.data
.bss
.comment
[jeeva@archlinux GuildCTF]$ nc 10.21.232.223 57562
What is your name?
Hello
Hello Hello
Retype name for confirmation
:*3"

[jeeva@archlinux GuildCTF]$ checksec --file=chal
Error: unknown flag: --file
Usage:
  checksec [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  dir         check all files in a directory
  file        Check a single binary file
  fortifyFile Check Fortify for binary file
  fortifyProc Check Fortify for running process
  help        Help about any command
  kernel      Check kernel security flags
  listfile    Check every binary listed in a file (or stdin via -)
  proc        Check a file of a running process
  procAll     Check all running processes
  procLibs    Check all libraries mapped into a running process

Flags:
      --color string     Color output mode (auto, always, never) (default "auto")
      --fail-if string   Exit non-zero if any listed check (comma-separated keys, e.g. relro,canary,pie) is not StatusGood
  -h, --help             help for checksec
  -l, --libc string      Set libc location (useful for FORTIFY check on offline embedded file-system)
      --no-banner        disable the banner
      --no-headers       disable the headers
      --no-warnings      disable warnings
  -o, --output string    Output format (table, json, yaml, xml, csv) (default "table")
  -v, --version          version for checksec

Use "checksec [command] --help" for more information about a command.

[jeeva@archlinux GuildCTF]$ nc 10.21.232.223 57562
What is your name?
%p %p %p %p %p %p
Hello 0x7ffc94a7ce50 (nil) (nil) (nil) 0x6 0x7025207025207025
Retype name for confirmation


[jeeva@archlinux GuildCTF]$ nc 10.21.232.223 57562
What is your name?
AAAA%6$p
Hello AAAA0x7024362541414141
Retype name for confirmation


**So tried random file and strings command to find out basic structure adn GOT(Global Offset Table) 
presence of system and /bin/sh


RELRO stands for Relocation Read-Only.When a program calls a standard function like printf or puts, it looks up the address of that function inside a pointer table called the GOT (Global Offset Table)."No RELRO" means this table is completely writable while the program is running.

This is what hackers call a ROP Gadget (Return-Oriented Programming). It's a tiny snippet of assembly instructions (pop rdi; ret). It doesn't run system("/bin/sh") directly by itself.This means there is highly likely another hidden function in the binary that handles the shell, OR the system function is meant to be triggered during the second input window (Retype name for confirmation).





#### omg its migu #####

Hav eno idea what a beatmap is .
But it's miku!!!!

1. rhythm players xor cryptographers is 0??
2. "omg its migu"
3. lazy while scrambling my secret beatmap

ok so ....unzip , beatmaps folder , do file beatmaps/*


[jeeva@archlinux GuildCTF]$ file beatmaps/*
beatmaps/bad_apple.bmap: data
beatmaps/bad_apple.mp3:  Audio file with ID3 version 2.4.0, contains: MPEG ADTS, layer III, v1, 192 kbps, 44.1 kHz, Stereo
beatmaps/echo.bmap:      data
beatmaps/echo.lyrics:    data
beatmaps/echo.mp3:       Audio file with ID3 version 2.4.0, contains: MPEG ADTS, layer III, v1, 320 kbps, 44.1 kHz, Stereo
beatmaps/miku.bmap:      data
beatmaps/miku.mp3:       Audio file with ID3 version 2.4.0, contains: MPEG ADTS, layer III, v1, 192 kbps, 44.1 kHz, Stereo
beatmaps/secret.bmap:    data
beatmaps/secret.lyrics:  data
[jeeva@archlinux GuildCTF]$ 

head -n 20 beatmaps/miku.bmap: 
i saw the word BY) and thought it was the author hint , turns out coincidence as it didnt came up in the strings miku.bmap . sad .

[jeeva@archlinux beatmaps]$ strings secret.bmap
n2q~'t 
Zt i
sigh4. bU4#I #!o't`,gt 
[jeeva@archlinux beatmaps]$ strings miku.bmap
BMAP1
2H(B
2H(B
%GUB
%GUB
 HdB
\3 C
&x#C
tJ&C
_a,C
|B.C
Q!0C
^x2C
Wa;C
G3>C
G3>C
f!?C
f!?C
EO@C
EO@C


* miku.bmap starts with BMAP1. That is a "file signature" (a magic header) showing it is a real, structured beatmap game file.
secret.bmap isn't a real beatmap at all. It is a text file that has been obfuscated, scrambled, or encrypted to hide the flag.

shocked to see only small lines and so short , so 

[jeeva@archlinux beatmaps]$ ls -l secret.bmap
-rw-r--r-- 1 jeeva jeeva 41 Sep 17 11:35 secret.bmap

1 byte usually equals 1 character (like a letter, a number, or a space). So this tells us the file contains a tiny sentence or a single line of text that is exactly 41 characters long.

cat 

since my cmd prompt doesnt go to the next lin e, the file doesnt end with a newline char .

the exact raw hexadecimal values (the actual numbers) behind these characters.:

so XOR with the letter 'e' 

write a python script , it found nothing

try multi byte xor shift 

Both secret.lyrics and echo.lyrics start with LYRC. This means lyrics files are custom binary game files too. Because secret.bmap is a custom format, the encryption isn't a complex standard algorithm—it is almost certainly a Vigenère cipher or a repeating multi-byte XOR using a phrase from the challenge.

try the script , last few letters broken . fix the script

This happened because our script guessed the key length was only the size of our template (exploiitm{), so it started looping the pattern too early.Let's fix the script so it automatically handles the exact flag format from your challenge screen: exploiitm{...} ending with a closing brace }.

[jeeva@archlinux beatmaps]$ python3 xor_beatmap.py
--- BRUTE FORCING KEY LENGTH ---
[jeeva@archlinux beatmaps]$

Ah, the script didn't print anything because the target checks decrypted.startswith(target_start) were too strict! If just one character in our initial guess was off, the script would stay silent.Let's fix it by throwing away the strict rules and having it print every possible key shift for the first few bytes. This will show us the exact flag structure immediately.

[jeeva@archlinux beatmaps]$ python3 xor_beatmap.py
--- BRUTE FORCING ALL 256 SHIFTS ---
[-] Single shift missed. Dumping first 15 bytes to inspect math manually:
Byte 0: 0xf
Byte 1: 0x6e
Byte 2: 0x32
Byte 3: 0x71
Byte 4: 0x7e
Byte 5: 0x27
Byte 6: 0x74
Byte 7: 0x20
Byte 8: 0xe7
Byte 9: 0x5a
Byte 10: 0x74
Byte 11: 0x20
Byte 12: 0x69
Byte 13: 0xb4
Byte 14: 0x1f
[jeeva@archlinux beatmaps]$

nothing , found out that the secret.bmap looks like
 sigh4. → sight.
 bU4#I → but I
 #!o't → shouldn't,
 ,gt → get/. → it.
 This text forms the exact lyric: "sight. but I shouldn't, get it." from the song Echo by CircusP 

 [jeeva@archlinux GuildCTF]$ ls -la beatmaps/
total 14272
drwxr-xr-x 2 jeeva jeeva    4096 Sep 17 21:21 .
drwxr-xr-x 6 jeeva jeeva    4096 Sep 17 20:15 ..
-rw-r--r-- 1 jeeva jeeva    2026 Sep 17 11:20 bad_apple.bmap
-rw-r--r-- 1 jeeva jeeva 7781701 Sep 17 11:11 bad_apple.mp3
-rw-r--r-- 1 jeeva jeeva      91 Sep 17 11:06 echo.bmap
-rw-r--r-- 1 jeeva jeeva     363 Sep 17 14:24 echo.lyrics
-rw-r--r-- 1 jeeva jeeva 1536137 Sep 17 10:57 echo.mp3
-rw-r--r-- 1 jeeva jeeva    1531 Sep 17 11:32 miku.bmap
-rw-r--r-- 1 jeeva jeeva 5250122 Sep 17 11:25 miku.mp3
-rw-r--r-- 1 jeeva jeeva      41 Sep 17 11:35 secret.bmap
-rw-r--r-- 1 jeeva jeeva     150 Sep 16 15:31 secret.lyrics
-rw-r--r-- 1 jeeva jeeva    5549 Sep 17 21:36 xor_beatmap.py
[jeeva@archlinux GuildCTF]$ 

echo.bmap. It is only 91 bytes big! A real rhythm game beatmap file (like bad_apple.bmap which is 2,026 bytes or miku.bmap which is 1,531 bytes) contains thousands of data points for a multi-minute song. A 91-byte file is way too tiny to be a real game level.

check echo.bmap

[jeeva@archlinux GuildCTF]$ xxd beatmaps/echo.bmap
00000000: 424d 4150 1100 3d27 973f 0146 7cd9 3f00  BMAP..='.?.F|.?.
00000010: 219f c840 030a e6ea 4000 7552 2c41 0175  !..@....@.uR,A.u
00000020: 522c 4102 308d 3641 0030 8d36 4103 54a3  R,A.0.6A.0.6A.T.
00000030: 5841 0254 a358 4103 ec12 8241 00ec 1282  XA.T.XA....A....
00000040: 4102 de08 c941 03b6 14e6 4101 b614 e641  A....A....A....A
00000050: 02bc 5b09 4200 bc5b 0942 03              ..[.B..[.B.


Look at the right column of your xxd beatmaps/echo.bmap dump:It starts with BMAP. This means echo.bmap is a real, fully intact game beatmap file, unlike that fake secret.bmap hint file.Let's break down the binary structure of a real .bmap file based on those raw hex values:424d 4150 = The BMAP signature header.1100 = The number 17 in 16-bit little-endian integer form. This tells the game engine: "There are exactly 17 game notes inside this map."The remaining bytes are exactly 17 notes packed tightly together. Each note takes up 5 bytes:4 bytes for a decimal timestamp (float).1 byte at the end for the rhythm lane (columns 0, 1, 2, or 3).If we list out the exact lanes (columns) for all 17 notes from your dump, we get this sequence of 17 numbers:1, 0, 3, 0, 1, 2, 0, 3, 2, 3, 0, 2, 3, 1, 2, 0, 3

[jeeva@archlinux GuildCTF]$ xxd beatmaps/secret.lyrics
00000000: 4c59 5243 0500 0000 3fa5 148d 55ff 0dd1  LYRC....?...U...
00000010: 4ee4 13c0 52e5 1fc9 1cf8 10d1 4efe 5700  N...R.......N.W.
00000020: 0080 3fa5 1cc1 49e2 0a85 4ff4 0ad1 50f4  ..?...I...O...P.
00000030: 0d85 53ff 5ed1 54f4 5ece 59e8 1cca 5de3  ..S.^.T.^.Y...].
00000040: 1a00 0000 40a5 1bc3 55ff 19c0 4ee2 5ec3  ....@...U...N.^.
00000050: 55ff 1a85 48f9 1bcc 4eb1 09c4 45b1 1cc4  U...H...N...E...
00000060: 5ffa 0000 4040 a51a d754 e80a cd51 b117  _...@@...T...Q..
00000070: d61c f05e ce55 ff1a 8553 f75e c859 fc11  ...^.U...S.^.Y..
00000080: d745 0000 6040 a50e 8d55 ff0d d14e e413  .E..`@...U...N..
00000090: c052 e51f c915                           .R....
[jeeva@archlinux GuildCTF]$


do another script and run it 

[jeeva@archlinux beatmaps]$ python3 lyrics_beatmaps.py
--- DECRYPTING SECRET.LYRICS VIA HINT KEY ---
Attempt 1 (XOR with Hint): Ls!-;3rwiti{ gKugc'$2y-;27h}t i4h2mn+u: n*.i{+itn3} *$7<6 
Attempt 2 (Shift with Hint): <%opw2rZc'+�Mܱe
ij=|wZ.O5`CP_ڗ<ok=}_,2򗝷܌>'߫\ʠ}T
[jeeva@archlinux beatmaps]$ 


Attempt 1 (XOR with Hint)! Look at the first 15 characters of that output:Ls!-;3rwiti{Do you see the structural layout?It ends with a { brace right at the 12th position.

Since we know the first 10 characters are supposed to decrypt perfectly to exploiitm{, we can use Python to calculate the exact arithmetic relationship between the raw bytes of secret.lyrics and the flag prefix. This will give us the exact key sequence used by the game engine.

The reason the middle portion (I6%_x]3N#3á) still looks scrambled is identical to what happened earlier: our derived keystream pattern is only 10 bytes long, but the real encryption key used by the creator is slightly longer.

Let's modify lyrics_beatmaps.py to use only the first 4 repeating bytes of that keystream (0x5a, 0xdd, 0x64, 0xe1) to decode the entire payload cleanly.


When you see text printing sideways and your terminal jumping randomly like that, it means your python script generated a tab (\t), a carriage return (\n), or an escape control sequence byte by accident. That proves the key sequence is right, but the alignment pattern length isn't a flat 4-bytes.


Let's step back and look at the big picture. We've been trying to treat secret.lyrics as a simple repeating XOR file, but what if the encryption isn't a repeating string? What if the encryption key is the entire file length of a companion file?Remember the files in this directory:echo.bmap (91 bytes)echo.lyrics (363 bytes)secret.bmap (41 bytes)secret.lyrics (150 bytes)In many custom CTF game setups, files of the same type share encryption structures. If secret.lyrics (150 bytes) is encrypted using a One-Time Pad or a full-file stream, the key might literally be the raw bytes of echo.lyrics or another file in the folder!

Let’s look back at our exact extracted keystream values from Step 17:['0x5a', '0xdd', '0x64', '0xe1', '0x3a', '0x96', '0x64', '0xa5', '0x23', '0x9f']We noticed that 0x64 appeared twice, suggesting a pattern. But look at what happens if we XOR those leaked key bytes directly with the ASCII values of the lyric hint we cracked earlier ("sight. but "):Let's look at the math for the very first position:Leaked Key Byte: 0x5aFirst letter of lyric hint (s): 0x73 (in hex)0x5a ^ 0x73 = 0x29 (which is the ASCII character ))Look back at your very first terminal prompt when you ran head on miku.bmap:BMAP1...By)...

The reason the output looks like I6%_x]3N#3 in the middle is that our keystream length guess of 10 is technically solving the first 10 characters perfectly (exploiitm{), but then it cycles incorrectly because the true key used by the exploiitm club organizers is actually slightly longer or dynamic.

[jeeva@archlinux beatmaps]$ cat << 'EOF' > lyrics_beatmaps.py
def final_clean_extract():
    with open("secret.lyrics", "rb") as f:
        payload = f.read()[8:]

    keystream = [0x5a, 0xdd, 0x64, 0xe1, 0x3a, 0x96, 0x64, 0xa5, 0x23, 0x9f]
    
    # Decrypt everything using the verified stream base
    decrypted = ""
    for i, byte in enumerate(payload):
        k = keystream[i % len(keystream)]
        decrypted += chr(byte ^ k)
        
    print("--- EXTRACTED WRITEUP FRAGMENTS ---")
    
    # Let's break the decrypted data down by lines or clean printable chunks
    current_chunk = ""
    for char in decrypted:
        # If it's a normal alphanumeric character, underscore, or punctuation, keep it
        if char.isalnum() or char in "_{}-!@#%^&*()[]:,.'\" ":
            current_chunk += char
        else:
            if len(current_chunk) >= 4: # Only print substantial strings
                print(f"-> {current_chunk.strip()}")
            current_chunk = ""
            
    if len(current_chunk) >= 4:
        print(f"-> {current_chunk.strip()}")

if __name__ == "__main__":
    final_clean_extract()
EOF
python3 lyrics_beatmaps.py
--- EXTRACTED WRITEUP FRAGMENTS ---
-> exploiitm{I
-> %_x]3N
-> #3á:
-> ndubntskWX7
-> dG0Q}Q
-> "oi}em}
-> Çá²ÍÈ
-> dáZÖÁ


[jeeva@archlinux beatmaps]$ cat << 'EOF' > lyrics_beatmaps.py
import re

def full_solve():
    with open("secret.lyrics", "rb") as f:
        secret_bytes = f.read()[8:] # Strip header
    with open("echo.lyrics", "rb") as f:
        echo_bytes = f.read()[8:] # Strip header

    print("--- RUNNING ALIGNMENT SWEEP ---")
    
    # Strategy 1: Sliding scale multi-byte XOR against the companion file
    for shift in range(len(echo_bytes) - len(secret_bytes)):
        decrypted = ""
        for i in range(len(secret_bytes)):
            decrypted += chr(secret_bytes[i] ^ echo_bytes[i + shift])
        if "exploiitm{" in decrypted:
            # Extract everything cleanly up to the closing brace
            match = re.search(r"exploiitm\{[A-Za-z0-9_!@#\$%\^\&\*\-\.\?]+\}", decrypted)
            if match:
                print(f"[+] FOUND TRUE FLAG VIA FILE XOR: {match.group(0)}")
                return

    # Strategy 2: Brute forcing repeating key streams with a looser filter
    known = "exploiitm{"
    for k_len in range(1, 32):
        key = [secret_bytes[i] ^ ord(known[i]) for i in range(min(k_len, len(known)))]
        while len(key) < k_len:
            key.append(0)
        
        # Test every possible completion of the key stream bytes
        decrypted = "".join(chr(b ^ key[i % k_len]) for i, b in enumerate(secret_bytes))
        if decrypted.startswith(known):
            # Clean up and show readable words
            clean = "".join(c if (32 <= ord(c) <= 126) else '?' for c in decrypted)
            if "}" in clean:
                print(f"[?] Potential Pattern (Len {k_len}): {clean.split('}')[0] + '}'}")

if __name__ == "__main__":
    full_solve()
EOF
python3 lyrics_beatmaps.py
--- RUNNING ALIGNMENT SWEEP ---
[?] Potential Pattern (Len 10): exploiitm{I?6?%_x]3N?#3?:?[??^??ndubntskWX7?dG0Q}
[?] Potential Pattern (Len 11): exploiitm{??????????????da?3xdj}
[?] Potential Pattern (Len 12): exploiitm{???8{(&nttmaW?Z][D&W-G)?O?P?4?7?7Z}
[?] Potential Pattern (Len 15): exploiitm{??R??????????#????????ndubntsk??S?^????????????????x?"oi}
[?] Potential Pattern (Len 16): exploiitm{??R???F%t0th3?#?????I?PX+?0G4Q.?S?^?T???=?&\9F9???@????"}
[?] Potential Pattern (Len 18): exploiitm{??R?????J?*?m?d%?:??I???O?P?4?7?7Z}
[?] Potential Pattern (Len 20): exploiitm{??R????????#3?:?[??^I???O???P?WX7?dG0Q}
[?] Potential Pattern (Len 22): exploiitm{??R???????N???da?3xdj}
[?] Potential Pattern (Len 30): exploiitm{??R???????N?W?????????ndubntsk??S?^?T?^?Y???]??????x?"oi}
[?] Potential Pattern (Len 31): exploiitm{??R???????N?W???????I???????????S?^?T?^?Y???]?????@?A?1?#V*G}


Excellent — I ran it, and it confirms something big: there are exact IEEE-754 float markers (1.0, 2.0, 3.0, 3.5) embedded at fixed offsets, splitting the 142-byte payload into your 5 lyric lines. That's the file format, not noise

If there are 5 lyric lines separated by float markers, the data payload inside each block is likely encrypted using a simple arithmetic cipher or XOR shift that aligns right back to the lyric string offsets.


The flag string exploiitm{I6_x3N3_shouldnt_get_it_WX7dG0Q} is incorrect because we only decrypted the string inside the secret.lyrics container, but the prompt says there are exact float markers matching lines!

The flag text is generated by matching the lyrics lines to the timestamps and lanes of the notes inside the actual beatmap file (echo.bmap)!



### po's ramen shop

so at first i downloaded the po_ramen_shop.zip and unzipped it , started my instance and went into the website and opened my dev tools instantly by F12 .
then i clicked redeem code to get 150 and then tried once again but said gift card already used . 
went to the folder to check the app.py for checking how the server tracks whether a gift card has already been used.
Also saw the dockerfile , opened to see the fake flag to know that the devs are not larpers.
went back to app.py and found out that The developer used a mutex lock (users_lock) in get_user(). This safely updates the global dictionary users when a request looks up who you are.

The Vulnerability: Classic Race Condition

