# mania!!

A 4-key rhythm game. Hit the notes, keep your accuracy up, see what happens.

## What you have

```
mania_game        the game
beatmaps/         the songs (.bmap charts + .mp3 audio)
README.md         this file
```

Keep these together. The game looks for `beatmaps/` **relative to the folder you
run it from**, so don't move the binary out on its own.

## Linux

1. Install the runtime libraries (raylib itself is already built into the binary):

   Debian / Ubuntu / WSL:
   ```
   sudo apt update
   sudo apt install -y libgl1 libx11-6 libasound2
   ```
   Fedora:
   ```
   sudo dnf install -y mesa-libGL libX11 alsa-lib
   ```
   Arch:
   ```
   sudo pacman -S --needed libglvnd libx11 alsa-lib
   ```

2. Run it from inside the extracted folder:
   ```
   cd path/to/mania_game_folder
   chmod +x mania_game
   ./mania_game
   ```

`chmod +x` is only needed once, and only if the zip dropped the permission bit.

## Windows (via WSL)

The game is a Linux binary — it will not run under `cmd` or PowerShell. Use WSL2
with WSLg, which is what gives WSL a graphical display.

**You need Windows 11, or Windows 10 21H2+ with WSL updated.** Check from
PowerShell:
```
wsl --version
wsl --update
```
If `wsl --version` prints nothing, you're on the old WSL1-era build — run
`wsl --update`, then `wsl --shutdown`, then reopen your distro.

Then, inside your WSL terminal (Ubuntu by default):

```
sudo apt update
sudo apt install -y libgl1 libx11-6 libasound2

cd /mnt/c/Users/<you>/Downloads/mania_game_folder
chmod +x mania_game
./mania_game
```

A game window should open on your Windows desktop.

Two things worth knowing:

- Running straight off `/mnt/c/...` works but is slow to load the audio. If the
  song stutters, copy the folder into the Linux filesystem first:
  `cp -r . ~/mania && cd ~/mania && ./mania_game`
- If you get a black window or a GL/driver error, force software rendering:
  `LIBGL_ALWAYS_SOFTWARE=1 ./mania_game`

## Controls

`D` `F` `J` `K` for the four lanes. Arrow keys and `Enter` to pick a song,
`Esc` to back out. On the results screen, `R` retries and `M` returns to the
menu.

## If it doesn't start

| What you see | What it means |
|---|---|
| `cannot execute binary file` | You're in cmd/PowerShell, not WSL. |
| `Permission denied` | `chmod +x mania_game` |
| `error while loading shared libraries: libGL.so.1` | Install step skipped — see above. |
| `No .bmap files found in 'beatmaps/'` | You ran it from the wrong directory. `cd` into the folder that holds `beatmaps/` first. |
| Window opens, no sound | WSL: make sure WSLg is up to date. Native Linux: install `libasound2`. |
| `GLFW: Failed to initialize GLFW` | No display available — you need a desktop session, not a bare SSH shell. |
