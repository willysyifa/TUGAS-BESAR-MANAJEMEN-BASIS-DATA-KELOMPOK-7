import re
import mysql.connector
from datetime import datetime

# =============================================
# KONFIGURASI KONEKSI KE DATABASE
# =============================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",        # XAMPP default kosong
    "database": "rme_db"
}

# =============================================
# KONFIGURASI RBAC
# role -> daftar operasi yang dibolehkan
# =============================================
RBAC_PERMISSIONS = {
    "admin":         ["SELECT", "INSERT", "UPDATE", "DELETE"],
    "dokter":        ["SELECT", "INSERT", "UPDATE"],
    "perawat":       ["SELECT", "INSERT"],
    "pasien":        ["SELECT"],
    "staf_keuangan": ["SELECT"]
}

# =============================================
# 18 POLA REGEX SQL INJECTION
# =============================================
SQLI_PATTERNS = [
    r"(\bOR\b\s+[\w'\"]+\s*=\s*[\w'\"]+)",     # OR 1=1 / OR 'a'='a'
    r"(\bAND\b\s+[\w'\"]+\s*=\s*[\w'\"]+)",    # AND 1=1
    r"(--\s*)",                                  # komentar --
    r"(/\*[\s\S]*?\*/)",                         # komentar /* */
    r"(\bUNION\b\s+\bSELECT\b)",               # UNION SELECT
    r"(\bDROP\b\s+\bTABLE\b)",                 # DROP TABLE
    r"(\bDROP\b\s+\bDATABASE\b)",              # DROP DATABASE
    r"(\bTRUNCATE\b\s+\bTABLE\b)",             # TRUNCATE TABLE
    r"(\bEXEC\b|\bEXECUTE\b)",                 # EXEC/EXECUTE
    r"(xp_cmdshell)",                           # stored procedure berbahaya
    r"(\bCAST\b\s*\()",                         # CAST()
    r"(\bCONVERT\b\s*\()",                      # CONVERT()
    r"(SLEEP\s*\(\s*\d+\s*\))",                 # SLEEP(n) - time-based
    r"(BENCHMARK\s*\()",                         # BENCHMARK()
    r"(\bWAITFOR\b\s+\bDELAY\b)",             # WAITFOR DELAY
    r"(0x[0-9a-fA-F]+)",                        # hex encoding
    r"(%27|%22|%3B|%3D)",                       # URL encoding berbahaya
    r"(;[\s]*\b(SELECT|INSERT|UPDATE|DELETE|DROP)\b)"  # stacked queries
]

def get_connection():
    """Buat koneksi ke database MySQL."""
    return mysql.connector.connect(**DB_CONFIG)

def detect_sqli(query: str) -> tuple:
    """
    Periksa apakah query mengandung pola SQL Injection.
    Return: (True/False, pola_yang_cocok)
    """
    for pattern in SQLI_PATTERNS:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return True, match.group()
    return False, None

def check_rbac(role: str, operation: str) -> bool:
    """
    Periksa apakah role punya izin untuk operasi tertentu.
    """
    allowed_ops = RBAC_PERMISSIONS.get(role, [])
    return operation.upper() in allowed_ops

def log_activity(username, query, action_type, status, reason=""):
    """Catat semua aktivitas query ke audit_log."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO audit_log (username, query_text, action_type, status)
            VALUES (%s, %s, %s, %s)
        """, (username, query[:500], action_type, f"{status}: {reason}" if reason else status))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[LOG ERROR] Gagal catat log: {e}")

def execute_query(username: str, role: str, query: str) -> dict:
    """
    Fungsi utama middleware.
    Urutan: cek RBAC → cek SQLi → eksekusi → log
    """
    operation = query.strip().split()[0].upper()

    # --- CEK RBAC ---
    if not check_rbac(role, operation):
        log_activity(username, query, operation, "BLOCKED", f"Role '{role}' tidak boleh {operation}")
        return {
            "status": "BLOCKED",
            "reason": f"Akses ditolak: role '{role}' tidak memiliki izin untuk operasi {operation}",
            "latency_ms": 0
        }

    # --- CEK SQL INJECTION ---
    is_sqli, matched_pattern = detect_sqli(query)
    if is_sqli:
        log_activity(username, query, operation, "SQLI_BLOCKED", f"Pattern: {matched_pattern}")
        return {
            "status": "SQLI_BLOCKED",
            "reason": f"SQL Injection terdeteksi! Pattern: {matched_pattern}",
            "latency_ms": 0
        }

    # --- EKSEKUSI QUERY AMAN ---
    try:
        conn = get_connection()
        cur = conn.cursor()
        start = datetime.now()
        cur.execute(query)
        latency_ms = (datetime.now() - start).total_seconds() * 1000
        rows = cur.fetchall() if operation == "SELECT" else []
        conn.commit()
        cur.close()
        conn.close()
        log_activity(username, query, operation, "ALLOWED")
        return {
            "status": "ALLOWED",
            "latency_ms": round(latency_ms, 4),
            "rows_affected": len(rows),
            "data": rows[:5]  # tampilkan max 5 baris
        }
    except Exception as e:
        log_activity(username, query, operation, "ERROR", str(e))
        return {"status": "ERROR", "reason": str(e), "latency_ms": 0}