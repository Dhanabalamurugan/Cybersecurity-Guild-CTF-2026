#!/usr/bin/env python3
"""
GuildCTF - rhythm game "secret.lyrics" keystream breaker.

Usage:
    python3 break_lyrics.py /path/to/challenge/folder
    python3 break_lyrics.py .            --deep      # bigger PRNG seed sweep
    python3 break_lyrics.py . --target secret.lyrics

No third-party deps. Python 3.8+.

Strategy (in order of how likely each is to actually work):
  A. Keystream reuse across files  <-- most likely win. secret.bmap has a KNOWN
     plaintext, so it leaks ~31 keystream bytes. If the same stream encrypts
     secret.lyrics, you get the whole flag immediately.
  B. Raw file-as-keypad (one file's bytes used as the pad for another).
  C. Repeating key of length 10..32, first 10 bytes known, rest solved per column.
  D. Counter-mixed variants of the leaked 10 bytes (ks[i%10] ^ i, + block, ...).
  E. Per-line keystream resets (5-line header) - find reset offsets.
  F. PRNG brute force (MSVC/glibc/minstd/Java LCGs, xorshift, Python random).
  G. Hash-derived streams: md5/sha1/sha256 of song/file/word candidates + chains.
  H. Byte-recurrence keystreams (ks[i] = a*ks[i-1]+c mod 256, etc.).
  I. Crib dragging against the companion ciphertext (echo.lyrics).
All attacks are run for XOR *and* for additive/subtractive (ASCII shift) ciphers.
"""

import argparse
import hashlib
import random
import string
import sys
from pathlib import Path

# ---------------------------------------------------------------- known facts
KS10 = bytes([0x5A, 0xDD, 0x64, 0xE1, 0x3A, 0x96, 0x64, 0xA5, 0x23, 0x9F])
FLAG_PREFIX = b"exploiitm{"
BMAP_PT = b"sight. but I shouldn't, get it."

# Add any other plaintext you are confident about (other lyric lines, etc.)
EXTRA_CRIBS = [
    FLAG_PREFIX,
    BMAP_PT,
    b"exploiitm{",
    b"CircusP",
    b"Echo",
]

RESULTS = []          # (score, tag, text, note)
SEEN = set()

# ------------------------------------------------------------------ utilities
COMMON_WORDS = (
    "the and you that this with have not but for are was all can get out was "
    "shouldn sight echo flag your just like know time what when there here "
    "line lyrics song level note beat play score chart hidden secret"
).split()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def sub(a: bytes, b: bytes) -> bytes:
    return bytes((x - y) & 0xFF for x, y in zip(a, b))


def add(a: bytes, b: bytes) -> bytes:
    return bytes((x + y) & 0xFF for x, y in zip(a, b))


def pretty(b: bytes) -> str:
    return "".join(chr(c) if 32 <= c < 127 else ("\\n" if c == 10 else ".") for c in b)


def score(data: bytes) -> float:
    """Rough English-text plausibility, normalised to length."""
    if not data:
        return -1e9
    s = 0.0
    for ch in data:
        if ch == 32 or 97 <= ch <= 122:
            s += 2.0
        elif ch == 10:
            s += 1.5
        elif 65 <= ch <= 90:
            s += 1.4
        elif 48 <= ch <= 57:
            s += 1.0
        elif ch in b".,'!?-_{}():;\"/":
            s += 0.9
        elif 32 <= ch < 127:
            s += 0.1
        else:
            s -= 6.0
    s /= len(data)
    low = data.lower().decode("latin1")
    for w in COMMON_WORDS:
        if w in low:
            s += 0.25
    if b"exploiitm{" in data:
        s += 6.0
    if b"}" in data and b"exploiitm{" in data:
        s += 4.0
    return s


def report(tag: str, data: bytes, note: str = ""):
    if not data:
        return
    key = (tag[:40], bytes(data[:64]))
    if key in SEEN:
        return
    SEEN.add(key)
    RESULTS.append((score(data), tag, data, note))


def printable_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    ok = sum(1 for c in data if 32 <= c < 127 or c in (9, 10, 13))
    return ok / len(data)


# --------------------------------------------------------------- keystream ops
def ks_apply(ct: bytes, ks: bytes, mode: str) -> bytes:
    n = min(len(ct), len(ks))
    if mode == "xor":
        return xor(ct[:n], ks[:n])
    if mode == "sub":
        return sub(ct[:n], ks[:n])
    if mode == "add":
        return add(ct[:n], ks[:n])
    raise ValueError(mode)


def ks_derive(ct: bytes, pt: bytes, mode: str) -> bytes:
    n = min(len(ct), len(pt))
    if mode == "xor":
        return xor(ct[:n], pt[:n])
    if mode == "sub":          # ct = pt + ks  -> ks = ct - pt
        return sub(ct[:n], pt[:n])
    if mode == "add":          # ct = pt - ks  -> ks = pt - ct
        return sub(pt[:n], ct[:n])
    raise ValueError(mode)


MODES = ("xor", "sub", "add")


# =============================================================== A. reuse
def attack_reuse(files, target, tgt_off):
    """secret.bmap has known plaintext -> leaks a long keystream. Try it on the
    target at every alignment, and check whether KS10 appears inside it."""
    ct_t = target[tgt_off:]
    pt_variants = [
        BMAP_PT, BMAP_PT + b"\n", BMAP_PT + b"\x00", b"\n" + BMAP_PT,
        BMAP_PT.lower(), BMAP_PT.capitalize(), BMAP_PT.replace("'", "\u2019".encode()[0:1] * 0 + b"'"),
    ]
    pt_variants = [p for p in pt_variants if p]

    for name, blob in files.items():
        for pt in pt_variants:
            if len(blob) < len(pt):
                continue
            for off in range(0, len(blob) - len(pt) + 1):
                for mode in MODES:
                    ks = ks_derive(blob[off:off + len(pt)], pt, mode)
                    if len(ks) < 8:
                        continue
                    # Decisive test: does the leaked 10-byte stream sit inside?
                    idx = ks.find(KS10)
                    if idx != -1:
                        print(f"[!!!] KS10 found inside keystream from {name} "
                              f"(pt off {off}, mode {mode}) at ks index {idx}")
                        stream = ks[idx:]
                        report(f"A-REUSE-EXACT {name} off={off} {mode}",
                               ks_apply(ct_t, stream, mode),
                               "KS10 matched inside derived keystream")
                    # generic: slide derived keystream over target
                    for toff in range(0, min(len(ct_t), 64)):
                        dec = ks_apply(ct_t[toff:], ks, mode)
                        if len(dec) >= 8 and printable_ratio(dec) > 0.92:
                            report(f"A-REUSE {name} ptoff={off} tgtoff={toff} {mode}",
                                   dec)


# =============================================================== B. file pads
def attack_file_pad(files, target, tgt_off, tname):
    ct = target[tgt_off:]
    for name, blob in files.items():
        if name == tname:
            continue
        for boff in range(0, min(len(blob), 40)):
            pad = blob[boff:]
            if len(pad) < 16:
                continue
            for mode in MODES:
                dec = ks_apply(ct, pad, mode)
                if len(dec) >= 16 and printable_ratio(dec) > 0.9:
                    report(f"B-PAD {name}+{boff} {mode}", dec)


# =============================================================== C. repeating
def solve_repeating(ct: bytes, L: int, mode: str):
    key = list(KS10[:L]) if L <= len(KS10) else list(KS10) + [None] * (L - len(KS10))
    for p in range(len(key)):
        if key[p] is not None:
            continue
        col = ct[p::L]
        best, best_sc = 0, -1e9
        for k in range(256):
            dec = ks_apply(col, bytes([k]) * len(col), mode)
            sc = score(dec) + (3.0 if printable_ratio(dec) == 1.0 else 0.0)
            if sc > best_sc:
                best, best_sc = k, sc
        key[p] = best
    keyb = bytes(key)
    full = (keyb * (len(ct) // L + 2))[:len(ct)]
    return keyb, ks_apply(ct, full, mode)


def attack_repeating(target, tgt_off):
    ct = target[tgt_off:]
    for L in range(10, 33):
        for mode in MODES:
            keyb, dec = solve_repeating(ct, L, mode)
            report(f"C-REPEAT L={L} {mode}", dec, f"key={keyb.hex()}")
    # also plain KS10 loop for reference
    for mode in MODES:
        full = (KS10 * (len(ct) // 10 + 2))[:len(ct)]
        report(f"C-REPEAT L=10 {mode}", ks_apply(ct, full, mode))


def index_of_coincidence(ct: bytes, period: int) -> float:
    ics = []
    for i in range(period):
        col = ct[i::period]
        if len(col) < 2:
            continue
        counts = {}
        for c in col:
            counts[c] = counts.get(c, 0) + 1
        n = len(col)
        ics.append(sum(v * (v - 1) for v in counts.values()) / (n * (n - 1)))
    return sum(ics) / len(ics) if ics else 0.0


# =============================================================== D. counters
def attack_counter_variants(target, tgt_off):
    ct = target[tgt_off:]
    n = len(ct)
    gens = {
        "ks[i%10]":            lambda i: KS10[i % 10],
        "ks[i%10]^i":          lambda i: KS10[i % 10] ^ (i & 0xFF),
        "ks[i%10]+i":          lambda i: (KS10[i % 10] + i) & 0xFF,
        "ks[i%10]-i":          lambda i: (KS10[i % 10] - i) & 0xFF,
        "ks[i%10]^(i//10)":    lambda i: KS10[i % 10] ^ (i // 10),
        "ks[i%10]+(i//10)":    lambda i: (KS10[i % 10] + i // 10) & 0xFF,
        "ks[i%10]-(i//10)":    lambda i: (KS10[i % 10] - i // 10) & 0xFF,
        "ks[i%10]^(i*i)":      lambda i: KS10[i % 10] ^ ((i * i) & 0xFF),
        "ks[9-i%10]":          lambda i: KS10[9 - (i % 10)],
        "ks[i%10]^ks[(i//10)%10]": lambda i: KS10[i % 10] ^ KS10[(i // 10) % 10],
        "ks[i%10]+ks[(i//10)%10]": lambda i: (KS10[i % 10] + KS10[(i // 10) % 10]) & 0xFF,
        "rotating ks":         lambda i: KS10[(i + i // 10) % 10],
    }
    for label, f in gens.items():
        stream = bytes(f(i) for i in range(n))
        for mode in MODES:
            report(f"D-CTR {label} {mode}", ks_apply(ct, stream, mode))


# =============================================================== E. per-line
def attack_line_resets(target, tgt_off, nlines):
    """If the keystream restarts per lyric line, KS10 (or its first bytes)
    should decrypt each line start into readable ASCII."""
    ct = target[tgt_off:]
    print("\n[*] Candidate keystream-reset offsets (KS10 gives clean ASCII):")
    cands = []
    for off in range(0, len(ct) - 6):
        chunk = ct[off:off + 10]
        for mode in MODES:
            dec = ks_apply(chunk, KS10, mode)
            if printable_ratio(dec) == 1.0 and score(dec) > 1.4:
                cands.append((off, mode, dec))
    for off, mode, dec in cands[:60]:
        print(f"    payload+{off:4d} {mode}: {pretty(dec)!r}")

    # brute: assume equal-ish split into nlines blocks, keystream restarts
    if nlines > 0:
        blk = len(ct) // nlines
        for extra in range(-4, 5):
            b = blk + extra
            if b <= 0:
                continue
            for mode in MODES:
                out = bytearray()
                for i in range(nlines):
                    part = ct[i * b:(i + 1) * b]
                    ks = (KS10 * (len(part) // 10 + 2))[:len(part)]
                    out += ks_apply(part, ks, mode)
                report(f"E-LINES blk={b} {mode}", bytes(out))

    # length-prefixed lines: 1/2/4-byte little endian lengths
    for plen in (1, 2, 4):
        for mode in MODES:
            out = bytearray()
            pos = 0
            ok = True
            for _ in range(nlines):
                if pos + plen > len(ct):
                    ok = False
                    break
                ln = int.from_bytes(ct[pos:pos + plen], "little")
                pos += plen
                if not (0 < ln <= len(ct) - pos):
                    ok = False
                    break
                part = ct[pos:pos + ln]
                pos += ln
                ks = (KS10 * (len(part) // 10 + 2))[:len(part)]
                out += ks_apply(part, ks, mode) + b"\n"
            if ok and out:
                report(f"E-LENPFX {plen}B {mode}", bytes(out))


# =============================================================== F. PRNGs
def prng_streams(seed, deep=False):
    """Yield (label, first-N-bytes) for a bunch of classic generators."""
    N = 200
    # MSVC rand()
    s = seed & 0xFFFFFFFF
    out1, out2 = bytearray(), bytearray()
    for _ in range(N):
        s = (s * 214013 + 2531011) & 0xFFFFFFFF
        r = (s >> 16) & 0x7FFF
        out1.append(r & 0xFF)
        out2.append((r >> 7) & 0xFF)
    yield "msvc_rand&0xff", bytes(out1)
    yield "msvc_rand>>7", bytes(out2)

    # classic ANSI-C LCG
    s = seed & 0xFFFFFFFF
    o1, o2 = bytearray(), bytearray()
    for _ in range(N):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        o1.append(s & 0xFF)
        o2.append((s >> 16) & 0xFF)
    yield "ansi_lcg_low", bytes(o1)
    yield "ansi_lcg_hi16", bytes(o2)

    # minstd
    s = (seed % 2147483646) + 1
    o = bytearray()
    for _ in range(N):
        s = (s * 48271) % 2147483647
        o.append(s & 0xFF)
    yield "minstd", bytes(o)

    # Java LCG
    s = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)
    o = bytearray()
    for _ in range(N):
        s = (s * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        o.append((s >> 40) & 0xFF)
    yield "java_lcg", bytes(o)

    # xorshift32
    s = seed & 0xFFFFFFFF or 0x9E3779B9
    o = bytearray()
    for _ in range(N):
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= s >> 17
        s ^= (s << 5) & 0xFFFFFFFF
        o.append(s & 0xFF)
    yield "xorshift32", bytes(o)

    if deep:
        r = random.Random(seed)
        yield "py_random_randbytes", bytes(r.randrange(256) for _ in range(N))


def attack_prng(target, tgt_off, deep):
    ct = target[tgt_off:]
    limit = 1 << 22 if deep else 1 << 18
    print(f"\n[*] PRNG sweep, seeds 0..{limit} (use --deep for a wider sweep)...")

    hits = []
    # fast pre-filter on the first two keystream bytes
    for seed in range(limit):
        if seed and seed % 200000 == 0:
            print(f"    ...seed {seed}")
        for label, stream in prng_streams(seed, deep=False):
            if stream[0] == KS10[0] and stream[1] == KS10[1]:
                if stream[:10] == KS10:
                    hits.append((label, seed, stream))
                    print(f"[!!!] PRNG MATCH: {label} seed={seed}")

    # Python's Mersenne Twister (slower, smaller sweep)
    pysweep = 200000 if deep else 50000
    for seed in range(pysweep):
        r = random.Random(seed)
        st = bytes(r.randrange(256) for _ in range(10))
        if st == KS10:
            print(f"[!!!] python random.Random({seed}).randrange(256) matches")
            r = random.Random(seed)
            hits.append(("py_random", seed,
                         bytes(r.randrange(256) for _ in range(len(ct) + 16))))
        r = random.Random(seed)
        if hasattr(r, "randbytes") and r.randbytes(10) == KS10:
            print(f"[!!!] python random.Random({seed}).randbytes matches")
            r = random.Random(seed)
            hits.append(("py_randbytes", seed, r.randbytes(len(ct) + 16)))

    for label, seed, stream in hits:
        full = stream
        while len(full) < len(ct):
            full += stream
        for mode in MODES:
            report(f"F-PRNG {label} seed={seed} {mode}", ks_apply(ct, full, mode))


# =============================================================== G. hashes
def hash_candidates(files, tname):
    words = [
        "Echo", "echo", "CircusP", "circusp", "Echo CircusP", "CircusP Echo",
        "echo.lyrics", "secret.lyrics", "secret.bmap", "LYRC", "BMAP",
        "rhythm", "guildctf", "GuildCTF", "exploiitm", "osu", "beatmap",
        BMAP_PT.decode(), tname,
    ]
    words += list(files.keys())
    seeds = [w.encode() for w in words]
    seeds += [b"5", (5).to_bytes(4, "little"), (150).to_bytes(4, "little"),
              (41).to_bytes(4, "little"), b"\x4c\x59\x52\x43"]
    return seeds


def attack_hashes(files, target, tgt_off, tname):
    ct = target[tgt_off:]
    algos = {"md5": hashlib.md5, "sha1": hashlib.sha1,
             "sha256": hashlib.sha256, "sha512": hashlib.sha512}
    for seed in hash_candidates(files, tname):
        for aname, af in algos.items():
            d = af(seed).digest()
            if d[:10] == KS10:
                print(f"[!!!] HASH MATCH: {aname}({seed!r})")
            # repeating digest
            full = (d * (len(ct) // len(d) + 2))[:len(ct)]
            for mode in MODES:
                report(f"G-HASH {aname}({seed[:20]!r}) repeat {mode}",
                       ks_apply(ct, full, mode))
            # counter-mode digest chain: H(seed||i)
            stream = bytearray()
            i = 0
            while len(stream) < len(ct):
                stream += af(seed + str(i).encode()).digest()
                i += 1
            if bytes(stream[:10]) == KS10:
                print(f"[!!!] HASH-CTR MATCH: {aname}({seed!r}||i)")
            for mode in MODES:
                report(f"G-HASHCTR {aname}({seed[:20]!r}) {mode}",
                       ks_apply(ct, bytes(stream), mode))
            # chained digest: H(seed), H(H(seed)), ...
            stream = bytearray()
            cur = seed
            while len(stream) < len(ct):
                cur = af(cur).digest()
                stream += cur
            if bytes(stream[:10]) == KS10:
                print(f"[!!!] HASH-CHAIN MATCH: {aname} chain of {seed!r}")
            for mode in MODES:
                report(f"G-HASHCHAIN {aname}({seed[:20]!r}) {mode}",
                       ks_apply(ct, bytes(stream), mode))


# =============================================================== H. recurrence
def attack_recurrence(target, tgt_off):
    """ks[i] = (a*ks[i-1] + c) mod m, and a few xor-shift byte recurrences."""
    ct = target[tgt_off:]
    found = []
    for m in (256, 251, 257):
        for a in range(m):
            for c in range(m):
                s = KS10[0]
                ok = True
                for i in range(1, 10):
                    s = (a * s + c) % m
                    if (s & 0xFF) != KS10[i]:
                        ok = False
                        break
                if ok:
                    found.append((a, c, m))
    for a, c, m in found:
        print(f"[!!!] byte recurrence: ks[i] = ({a}*ks[i-1] + {c}) mod {m}")
        stream = bytearray([KS10[0]])
        s = KS10[0]
        while len(stream) < len(ct):
            s = (a * s + c) % m
            stream.append(s & 0xFF)
        for mode in MODES:
            report(f"H-REC a={a} c={c} m={m} {mode}",
                   ks_apply(ct, bytes(stream), mode))
    if not found:
        print("[*] No simple byte-LCG recurrence fits the leaked keystream.")


# =============================================================== I. crib drag
def attack_crib_drag(files, target, tgt_off, tname):
    """If two files share a keystream, ct1^ct2 = pt1^pt2. Drag cribs through it."""
    ct = target[tgt_off:]
    for name, blob in files.items():
        if name == tname or len(blob) < 16:
            continue
        for boff in (0, 4, 8, 12, 16):
            other = blob[boff:]
            n = min(len(ct), len(other))
            if n < 16:
                continue
            delta = xor(ct[:n], other[:n])
            print(f"\n[*] Crib drag: {tname}+{tgt_off} XOR {name}+{boff} ({n} bytes)")
            for crib in EXTRA_CRIBS:
                for pos in range(0, n - len(crib) + 1):
                    guess = xor(delta[pos:pos + len(crib)], crib)
                    if printable_ratio(guess) == 1.0 and score(guess) > 1.7:
                        print(f"    crib {crib[:16]!r} @{pos:3d} -> {pretty(guess)!r}")


# =============================================================== extras
def attack_bmap_cross_check(files, target, tgt_off):
    """Confirm whether secret.bmap's keystream really is the same stream."""
    for name, blob in files.items():
        if not name.endswith(".bmap"):
            continue
        print(f"\n[*] Cross-check {name} against the leaked KS10:")
        for off in range(0, min(len(blob), 24)):
            for mode in MODES:
                dec = ks_apply(blob[off:off + 10], KS10, mode)
                if printable_ratio(dec) == 1.0:
                    print(f"    {name}+{off} {mode}: {pretty(dec)!r}")


def brute_extend_from_flag(target, tgt_off):
    """Print the raw keystream implied if the whole payload were readable ASCII,
    which sometimes exposes the generator pattern by eye."""
    ct = target[tgt_off:]
    print("\n[*] Ciphertext payload hex (payload offset 0 = first flag byte):")
    for i in range(0, len(ct), 16):
        chunk = ct[i:i + 16]
        print(f"    {i:04d}  {chunk.hex(' ')}  {pretty(chunk)}")
    print("\n[*] Leaked keystream (payload 0..9):", KS10.hex(" "))
    print("[*] Deltas between consecutive keystream bytes:")
    print("    xor :", " ".join(f"{KS10[i] ^ KS10[i+1]:02x}" for i in range(9)))
    print("    sub :", " ".join(f"{(KS10[i+1]-KS10[i])&0xff:02x}" for i in range(9)))


# =============================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?", default=".")
    ap.add_argument("--target", default=None, help="ciphertext file to break")
    ap.add_argument("--deep", action="store_true", help="wider PRNG sweep (slow)")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        sys.exit(f"Not a directory: {folder}")

    files = {p.name: p.read_bytes() for p in sorted(folder.iterdir()) if p.is_file()}
    if not files:
        sys.exit("No files found.")

    print("[*] Files:")
    for n, b in files.items():
        print(f"    {n:24s} {len(b):5d} bytes  magic={b[:4]!r}")

    tname = args.target
    if tname is None:
        tname = "secret.lyrics" if "secret.lyrics" in files else next(
            (n for n in files if n.endswith(".lyrics")), None)
    if tname is None or tname not in files:
        sys.exit("Could not find a target file; pass --target NAME")
    target = files[tname]
    print(f"\n[*] Target: {tname} ({len(target)} bytes)")

    # header detection
    nlines = 5
    tgt_off = 0
    if target[:4] in (b"LYRC", b"BMAP", b"CHRT"):
        nlines = int.from_bytes(target[4:8], "little")
        tgt_off = 8
        print(f"[*] Header {target[:4]!r}, count={nlines}, payload offset {tgt_off}")

    # sanity: does KS10 sit at payload offset 0 or file offset 0?
    for cand in {0, tgt_off}:
        dec = ks_apply(target[cand:cand + 10], KS10, "xor")
        print(f"[*] XOR at file offset {cand}: {pretty(dec)!r}")
        if dec == FLAG_PREFIX:
            tgt_off = cand
    print(f"[*] Using payload offset {tgt_off}")

    brute_extend_from_flag(target, tgt_off)

    print("\n[*] Index of coincidence per candidate key length:")
    ct = target[tgt_off:]
    ics = [(index_of_coincidence(ct, L), L) for L in range(2, 33)]
    for ic, L in sorted(ics, reverse=True)[:8]:
        print(f"    L={L:2d}  IC={ic:.4f}")

    attack_bmap_cross_check(files, target, tgt_off)

    print("\n[*] A: keystream reuse from known-plaintext files...")
    attack_reuse(files, target, tgt_off)

    print("[*] B: raw file-as-pad...")
    attack_file_pad(files, target, tgt_off, tname)

    print("[*] C: repeating keys, length 10..32...")
    attack_repeating(target, tgt_off)

    print("[*] D: counter-mixed variants of the leaked bytes...")
    attack_counter_variants(target, tgt_off)

    print("[*] E: per-line keystream resets...")
    attack_line_resets(target, tgt_off, nlines)

    print("[*] H: byte recurrences...")
    attack_recurrence(target, tgt_off)

    print("[*] G: hash-derived keystreams...")
    attack_hashes(files, target, tgt_off, tname)

    print("[*] F: PRNG brute force...")
    attack_prng(target, tgt_off, args.deep)

    print("[*] I: crib dragging against companion ciphertexts...")
    attack_crib_drag(files, target, tgt_off, tname)

    # ------------------------------------------------------------- results
    RESULTS.sort(key=lambda r: -r[0])
    print("\n" + "=" * 78)
    print(f"TOP {args.top} CANDIDATE DECRYPTIONS")
    print("=" * 78)
    for sc, tag, data, note in RESULTS[:args.top]:
        print(f"\n[{sc:6.2f}] {tag}  {note}")
        print("        " + pretty(data)[:300])

    print("\n" + "=" * 78)
    flags = set()
    for _, _, data, _ in RESULTS:
        i = data.find(b"exploiitm{")
        while i != -1:
            j = data.find(b"}", i)
            if j != -1 and j - i < 120:
                flags.add(data[i:j + 1])
            i = data.find(b"exploiitm{", i + 1)
    if flags:
        print("COMPLETE FLAG CANDIDATES (full exploiitm{...} with closing brace):")
        for f in sorted(flags, key=len):
            print("   ", f.decode("latin1"))
    else:
        print("No complete flag recovered. Next steps:")
        print("  * Run with --deep for the wider PRNG sweep.")
        print("  * Add any other known plaintext to EXTRA_CRIBS at the top.")
        print("  * If a challenge binary exists, disassemble its keystream routine;")
        print("    a 10-byte non-ASCII stream that never repeats is almost always")
        print("    a seeded PRNG, and the seed is usually in the file header.")


if __name__ == "__main__":
    main()



