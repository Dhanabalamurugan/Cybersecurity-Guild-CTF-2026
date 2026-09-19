def get_clean_flag():
    # The clean characters extracted from the structural segments
    # stripped of the 4-byte IEEE-754 floating point markers
    prefix = "exploiitm{"
    
    # Segment 1: Inner string text before the drift
    part1 = "I6_x3N3"
    
    # Segment 2: The middle lyrics-aligned word
    part2 = "shouldnt_get_it"
    
    # Segment 3: The final structural hash closure
    part3 = "_WX7dG0Q"
    
    suffix = "}"
    
    print("\n=========================================")
    print("[+] STRUCTURAL ALIGNMENT COMPLETE!")
    print(f"    YOUR FLAG: {prefix}{part1}_{part2}{part3}{suffix}")
    print("=========================================\n")

if __name__ == "__main__":
    get_clean_flag()
