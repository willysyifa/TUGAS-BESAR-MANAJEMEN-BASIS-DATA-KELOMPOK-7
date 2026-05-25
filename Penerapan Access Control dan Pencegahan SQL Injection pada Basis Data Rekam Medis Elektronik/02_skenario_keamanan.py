from middleware import execute_query

print("=" * 60)
print("SKENARIO A: PENGUJIAN KEAMANAN")
print("=" * 60)

# --- Uji SQL Injection ---
print("\n[1] Uji SQL Injection Detection")
sqli_tests = [
    ("attacker", "pasien", "SELECT * FROM patients WHERE name='' OR 1=1 --"),
    ("attacker", "pasien", "SELECT * FROM patients UNION SELECT * FROM users-- "),
    ("attacker", "pasien", "'; DROP TABLE patients; --"),
    ("attacker", "pasien", "SELECT * FROM patients WHERE id=1 AND SLEEP(5)"),
    ("attacker", "pasien", "SELECT * FROM patients WHERE id=0x31"),
]

for username, role, query in sqli_tests:
    result = execute_query(username, role, query)
    print(f"  Query : {query[:60]}...")
    print(f"  Status: {result['status']} | Alasan: {result.get('reason','')}")
    print()

# --- Uji RBAC ---
print("\n[2] Uji RBAC - Akses Lintas Batas")
rbac_tests = [
    ("perawat_01", "perawat",       "DELETE FROM medical_records WHERE record_id=1"),
    ("pasien_01",  "pasien",        "INSERT INTO medical_records (patient_id) VALUES (1)"),
    ("keuangan_01","staf_keuangan", "UPDATE patients SET name='hacked' WHERE patient_id=1"),
    ("dokter_01",  "dokter",        "SELECT * FROM patients WHERE patient_id=1"),  # ini boleh
    ("admin_01",   "admin",         "DELETE FROM audit_log WHERE log_id=1"),        # ini boleh
]

for username, role, query in rbac_tests:
    result = execute_query(username, role, query)
    print(f"  User: {username} ({role})")
    print(f"  Query : {query[:60]}")
    print(f"  Status: {result['status']}")
    print()