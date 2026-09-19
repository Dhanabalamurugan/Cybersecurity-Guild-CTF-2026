def print_raw_clean():
    # The exact string from your stream
    raw_stream = "exploiitm{I6%_x]3N#3:[?^?ndubntskWX7dG0Q}"
    
    # Strip out the question marks that your terminal printed for hidden bytes
    clean_flag = raw_stream.replace("?", "")
    
    print("\n=========================================")
    print("[+] TRY THIS RAW STRING IN THE PORTAL:")
    print(f"    {clean_flag}")
    print("=========================================\n")

if __name__ == "__main__":
    print_raw_clean()
