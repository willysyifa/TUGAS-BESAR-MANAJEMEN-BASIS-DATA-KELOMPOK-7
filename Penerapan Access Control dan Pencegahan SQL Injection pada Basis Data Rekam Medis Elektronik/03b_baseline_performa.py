import threading
import time
import mysql.connector
import json

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "rme_db"
}

RBAC_PERMISSIONS = {
    "admin":         ["SELECT","INSERT","UPDATE","DELETE"],
    "dokter":        ["SELECT","INSERT","UPDATE"],
    "perawat":       ["SELECT","INSERT"],
    "pasien":        ["SELECT"],
    "staf_keuangan": ["SELECT"]
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def check_rbac(role, operation):
    return operation.upper() in RBAC_PERMISSIONS.get(role, [])

# =============================================
# BASELINE A: Tanpa keamanan sama sekali
# =============================================
def query_baseline_a(user_id, results_list):
    query = f"SELECT * FROM patients WHERE patient_id = {(user_id % 1000) + 1}"
    try:
        conn = get_connection()
        cur = conn.cursor()
        start = time.time()
        cur.execute(query)
        cur.fetchall()
        latency = (time.time() - start) * 1000
        conn.close()
        results_list.append({"latency_ms": round(latency, 2), "status": "OK"})
    except Exception as e:
        results_list.append({"latency_ms": 0, "status": "ERROR"})

# =============================================
# BASELINE B: Hanya RBAC, tanpa deteksi SQLi
# =============================================
def query_baseline_b(user_id, results_list):
    query = f"SELECT * FROM patients WHERE patient_id = {(user_id % 1000) + 1}"
    operation = query.strip().split()[0].upper()
    # Hanya cek RBAC, tidak ada cek SQLi
    if not check_rbac("dokter", operation):
        results_list.append({"latency_ms": 0, "status": "BLOCKED"})
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        start = time.time()
        cur.execute(query)
        cur.fetchall()
        latency = (time.time() - start) * 1000
        conn.close()
        results_list.append({"latency_ms": round(latency, 2), "status": "OK"})
    except Exception as e:
        results_list.append({"latency_ms": 0, "status": "ERROR"})

def run_test(func, n_users, label):
    results = []
    threads = [threading.Thread(target=func, args=(i, results)) for i in range(n_users)]
    start_time = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    total_time = time.time() - start_time
    tps = n_users / total_time
    avg_lat = sum(r["latency_ms"] for r in results) / len(results)
    max_lat = max(r["latency_ms"] for r in results)
    return {
        "sistem": label,
        "n_users": n_users,
        "tps": round(tps, 2),
        "avg_latency": round(avg_lat, 2),
        "max_latency": round(max_lat, 2)
    }

print("=" * 60)
print("BASELINE A & B — PERBANDINGAN PERFORMA")
print("=" * 60)

all_results = []
for n in [10, 50, 100, 200]:
    r_a = run_test(query_baseline_a, n, "Baseline A (Tanpa Keamanan)")
    r_b = run_test(query_baseline_b, n, "Baseline B (RBAC Saja)")
    all_results.append(r_a)
    all_results.append(r_b)
    print(f"\n--- {n} Concurrent Users ---")
    print(f"  Baseline A | TPS: {r_a['tps']:>8} | Avg Latency: {r_a['avg_latency']:>8} ms | Max: {r_a['max_latency']} ms")
    print(f"  Baseline B | TPS: {r_b['tps']:>8} | Avg Latency: {r_b['avg_latency']:>8} ms | Max: {r_b['max_latency']} ms")

# Simpan hasil ke file JSON supaya bisa dibaca visualisasi
with open("hasil_baseline.json", "w") as f:
    json.dump(all_results, f)

print("\nHasil disimpan ke hasil_baseline.json")