import threading
import time
from middleware import execute_query

print("=" * 60)
print("SKENARIO B: PENGUJIAN PERFORMA & SKALABILITAS")
print("=" * 60)

def simulate_user(user_id, results_list):
    query = f"SELECT * FROM patients WHERE patient_id = {(user_id % 1000) + 1}"
    start = time.time()
    result = execute_query(f"dokter_{user_id}", "dokter", query)
    latency = (time.time() - start) * 1000
    results_list.append({"user_id": user_id, "latency_ms": round(latency, 2), "status": result["status"]})

for n_users in [10, 50, 100, 200]:
    results = []
    threads = [threading.Thread(target=simulate_user, args=(i, results)) for i in range(n_users)]

    start_time = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    total_time = time.time() - start_time

    tps = n_users / total_time
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)
    max_latency = max(r["latency_ms"] for r in results)

    print(f"\nConcurrent Users : {n_users}")
    print(f"Total Waktu      : {total_time:.2f} detik")
    print(f"TPS              : {tps:.2f} transaksi/detik")
    print(f"Avg Latency      : {avg_latency:.2f} ms")
    print(f"Max Latency      : {max_latency:.2f} ms")