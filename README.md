# 🔐 Penerapan Access Control dan Pencegahan SQL Injection pada Basis Data Rekam Medis Elektronik

> Tugas Besar Manajemen Basis Data — Kelompok 7  
> Institut Teknologi Sumatera — Program Studi Teknik Informatika  
> Semester Genap 2025/2026

---

## 👥 Identitas Kelompok

**Dosen Pengampu:**
- Meida Cahyo Untoro, S.Kom., M.Kom.
- Raidah Hanifah, S.T., M.T.

| No | NIM | Nama | Kontribusi | % |
|---|---|---|---|:---:|
| 1 | 123140010 | Margaretta Angela Manulang | Kajian literatur access control, penyusunan Bab II (2.1 Tinjauan Studi Terkait), analisis konsep RBAC | 12,5% |
| 2 | 123140011 | Ade Putri Tifani | Penyusunan Bab I (1.1 Latar Belakang), identifikasi ancaman keamanan RME | 12,5% |
| 3 | 123140017 | Natasya Felisita Br Ginting | Kajian literatur SQL Injection, penyusunan Bab II (2.2 Tabel Perbandingan Studi Terdahulu) | 12,5% |
| 4 | 123140044 | Jesika Filosovi Br P-A | Penyusunan Bab I (1.3 Tujuan & Kontribusi), skenario pengujian RBAC | 12,5% |
| 5 | 123140062 | Nabila Ramadhani M. | Penyusunan Bab II (2.3 Research Gap), metodologi, dan daftar pustaka | 12,5% |
| 6 | 123140070 | Annisa Salsabila | Implementasi middleware Python, deteksi SQLi (18 regex), audit log, visualisasi hasil eksperimen | 12,5% |
| 7 | 123140071 | Willy Syifa Luthfia | Penyusunan Bab III–IV (metodologi & desain eksperimen), integrasi laporan, dokumentasi GitHub | 12,5% |
| 8 | 123140133 | Silvia | Penyusunan Bab I (1.2 Rumusan Masalah), Bab VI (Kesimpulan), validasi & konsistensi laporan | 12,5% |

---

## 📋 Deskripsi Proyek

Proyek ini mengimplementasikan sistem keamanan berlapis pada basis data **Rekam Medis Elektronik (RME)** melalui:

1. **Role-Based Access Control (RBAC)** — membatasi hak akses berdasarkan peran pengguna secara granular di level basis data.
2. **Deteksi SQL Injection** — menggunakan 18 pola *regex rule-based* untuk memblokir query berbahaya sebelum dieksekusi.

Sistem dibangun sebagai **security middleware berbasis Python** yang berfungsi sebagai *gatekeeper* antara pengguna dan MySQL, sesuai **UU PDP No. 27 Tahun 2022**.

---

## 🏗️ Arsitektur Sistem

```
Client Layer       Security Middleware (Python)        Database Layer
──────────────     ─────────────────────────────       ──────────────
admin              ┌──────────────────────────┐
dokter  ─────────► │  1. RBAC Checker          │──BLOCKED──► Akses Ditolak
perawat            │  2. SQL Injection Detector │
pasien             │  3. Audit Logger           │──ALLOWED──► MySQL rme_db
staf_keuangan      └──────────────────────────┘
```

---

## 🗂️ Struktur Direktori

```
├── middleware.py                  # Core: RBAC + SQLi detection + audit log
├── 01_import_data.py              # Import dataset ke MySQL
├── 02_skenario_keamanan.py        # Pengujian fungsional RBAC & SQLi
├── 03_skenario_performa.py        # Pengujian performa & skalabilitas
├── 03b_baseline_performa.py       # Baseline tanpa keamanan
├── 04_skenario_sqli_detection.py  # Evaluasi akurasi deteksi SQLi
├── 05_visualisasi.py              # Visualisasi hasil eksperimen
├── dataset/
│   ├── healthcare_dataset.csv     # 55.500 baris data pasien simulasi
│   └── sql_dataset.csv            # 30.919 query SQL berlabel
└── README.md
```

---
📁 **Link Github:** [Github Kelompok 7](https://github.com/)  
📄 **Link Laporan:** [Tugas Besar Kelompok 7 — Keamanan, Keandalan & Etika Data](https://drive.google.com/)

---

## ⚙️ Instalasi & Menjalankan

**Prasyarat:** Python 3.x, XAMPP (MySQL aktif)

```bash
# Install dependensi
pip install mysql-connector-python pandas scikit-learn matplotlib numpy

# Inisialisasi database
python 01_import_data.py

# Jalankan pengujian
python 02_skenario_keamanan.py
python 03_skenario_performa.py
python 04_skenario_sqli_detection.py
python 05_visualisasi.py
```

Konfigurasi koneksi di `middleware.py`: `host=localhost`, `user=root`, `database=rme_db`.

---

## 🔑 Kebijakan RBAC

| Peran | SELECT | INSERT | UPDATE | DELETE | Level |
|---|:---:|:---:|:---:|:---:|---|
| `admin` | ✅ | ✅ | ✅ | ✅ | Full Access |
| `dokter` | ✅ | ✅ | ✅ | ❌ | Read + Write |
| `perawat` | ✅ | ✅ | ❌ | ❌ | Read + Insert |
| `pasien` | ✅ | ❌ | ❌ | ❌ | Read Only |
| `staf_keuangan` | ✅ | ❌ | ❌ | ❌ | Read Only |

---

## 📊 Hasil Pengujian

| Metrik | Hasil |
|---|---|
| Akurasi RBAC | **100%** (5/5 skenario) |
| Detection Rate SQLi | **64,7%** (7.359 / 11.382 query berbahaya) |
| False Positive Rate | **3,6%** (711 / 19.537 query aman) |
| Throughput sistem penuh (200 user) | **526 TPS**, latency **34 ms** |
| Overhead vs baseline | **~15%** (masih dalam batas toleransi) |

---

## ⚠️ Keterbatasan

- Deteksi SQLi berbasis regex belum mengenali teknik obfuskasi atau pola serangan baru.
- Pengujian pada lingkungan simulasi, belum pada sistem rumah sakit nyata.
- MFA, enkripsi data sensitif, dan monitoring real-time belum diimplementasikan.

---

> **Institut Teknologi Sumatera — Teknik Informatika — 2026**
