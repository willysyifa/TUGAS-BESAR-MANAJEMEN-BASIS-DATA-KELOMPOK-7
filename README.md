# 🔐 Implementasi Role-Based Access Control (RBAC) dan Deteksi SQL Injection pada Basis Data Rekam Medis Elektronik

---

## 📌 Deskripsi Tugas Besar

Tugas besar ini merupakan project implementasi keamanan basis data pada sistem Rekam Medis Elektronik (RME) dengan fokus pada aspek keamanan, keandalan, dan perlindungan data pasien. Sistem dikembangkan menggunakan MySQL dan middleware Python untuk mensimulasikan bagaimana mekanisme keamanan diterapkan pada lingkungan layanan kesehatan yang memiliki data sensitif dan akses multi-user.

Penelitian ini dilatarbelakangi oleh tingginya risiko kebocoran data kesehatan akibat lemahnya kontrol akses dan serangan terhadap basis data, khususnya SQL Injection. Data rekam medis elektronik mengandung informasi pribadi pasien seperti identitas, riwayat penyakit, hasil pemeriksaan, diagnosis, dan informasi medis lainnya yang harus dilindungi dari akses ilegal maupun manipulasi data.

Pada project ini diterapkan dua mekanisme keamanan utama, yaitu:

- **Role-Based Access Control (RBAC)** untuk membatasi hak akses pengguna sesuai role masing-masing.
- **SQL Injection Detection berbasis Regular Expression (Regex)** untuk mendeteksi dan memblokir query SQL berbahaya sebelum dieksekusi ke database.

Selain itu, sistem juga dilengkapi dengan:
- Middleware keamanan berbasis Python
- Audit log untuk pencatatan aktivitas query
- Pengujian performa sistem
- Dashboard visualisasi hasil eksperimen

Project ini menggunakan:
- Dataset rekam medis elektronik sebanyak **55.500 data pasien**
- Dataset SQL Injection sebanyak **30.919 query**

Pengujian dilakukan menggunakan beberapa skenario keamanan untuk membandingkan efektivitas sistem:
1. Sistem tanpa keamanan
2. Sistem dengan RBAC saja
3. Sistem dengan RBAC + SQL Injection Detection

Hasil pengujian digunakan untuk mengevaluasi:
- Kemampuan deteksi SQL Injection
- Ketepatan pembatasan hak akses
- Akurasi audit log
- Dampak keamanan terhadap performa sistem

---

# 👥 Identitas Kelompok

| Kelompok | 7 |
|---|---|
| Mata Kuliah | Manajemen Basis Data |
| Program Studi | Teknik Informatika |
| Institusi | Institut Teknologi Sumatera (ITERA) |
| Semester | Genap 2025/2026 |
| Topik | Keamanan, Keandalan, dan Etika Data |

---

# 📋 Pembagian Tugas dan Kontribusi Kelompok

| No | Nama | NIM | Kontribusi Laporan & Implementasi |
|---|---|---|---|
| 1 | Margaretta Angela Manulang | 123140010 | Mencari dan menganalisis 2 jurnal utama terkait access control pada Electronic Health Record, menyusun Bab II bagian 2.1 Tinjauan Studi Terkait, membantu analisis teori keamanan basis data kesehatan, membantu penyusunan konsep Role-Based Access Control (RBAC), serta membantu validasi isi kajian literatur |
| 2 | Ade Putri Tifani | 123140011 | Mencari dan menganalisis 2 jurnal utama terkait keamanan database kesehatan, menyusun Bab I bagian 1.1 Latar Belakang, membantu identifikasi permasalahan keamanan data rekam medis elektronik, menyusun urgensi penelitian, serta membantu penyusunan deskripsi ancaman keamanan data kesehatan |
| 3 | Natasya Felisita Br Ginting | 123140017 | Mencari dan menganalisis 2 jurnal utama terkait SQL Injection dan keamanan database, menyusun Bab II bagian 2.2 Tabel Perbandingan Studi Terdahulu, membantu analisis metode penelitian terdahulu, membantu penyusunan research comparison, serta membantu analisis pendekatan SQL Injection Detection pada penelitian sebelumnya |
| 4 | Jesika Filosovi Br P-A | 123140044 | Mencari dan menganalisis 2 jurnal utama terkait RBAC dan keamanan sistem informasi kesehatan, menyusun Bab I bagian 1.3 Tujuan dan Kontribusi Penelitian, membantu penyusunan arah penelitian, membantu penyusunan manfaat penelitian, serta membantu penyusunan skenario pengujian keamanan dan validasi hak akses RBAC |
| 5 | Nabila Ramadhani Mujahidin | 123140062 | Mencari dan menganalisis 2 jurnal utama terkait privacy dan security healthcare system, menyusun Bab II bagian 2.3 Research Gap dan Posisi Penelitian, membantu penyusunan metodologi penelitian, membantu penyusunan daftar pustaka dan sitasi, serta membantu analisis gap penelitian dan posisi penelitian terhadap penelitian sebelumnya |
| 6 | Annisa Salsabila | 123140070 | Mencari dan menganalisis 2 jurnal pelengkap terkait SQL Injection Detection dan keamanan basis data, mengimplementasikan middleware keamanan berbasis Python, implementasi deteksi SQL Injection menggunakan regex, implementasi Role-Based Access Control (RBAC), implementasi audit log, pengolahan dataset healthcare dan SQL dataset, implementasi pengujian keamanan sistem, pengujian performa database, visualisasi hasil eksperimen menggunakan Python, pengelolaan GitHub repository, dokumentasi source code, serta membantu penyusunan Bab III, Bab IV, dan Bab V terkait implementasi sistem dan eksperimen |
| 7 | Willy Syifa Luthfia | 123140071 | Mencari dan menganalisis 2 jurnal pelengkap terkait keamanan basis data dan sistem informasi kesehatan, menyusun Bab I bagian 1.4 Struktur Paper, membantu penyusunan Bab III Desain Sistem, membantu dokumentasi eksperimen dan hasil pengujian, membantu integrasi keseluruhan isi laporan, membantu penyusunan dashboard visualisasi hasil, serta menyusun lampiran pembagian tugas dan dokumentasi penelitian |
| 8 | Silvia | 123140133 | Mencari dan menganalisis 2 jurnal pelengkap terkait keamanan data pribadi dan regulasi perlindungan data, menyusun Bab I bagian 1.2 Rumusan Masalah, membantu validasi isi laporan, membantu proofreading keseluruhan laporan, membantu pengecekan konsistensi format penulisan, serta membantu penyusunan Bab VI Kesimpulan, Keterbatasan Penelitian, dan Rencana Pengembangan sistem |

---
# 📊 Persentase Kontribusi

| Nama | Persentase Kontribusi |
|---|---|
| Margaretta Angela Manulang | 12.5% |
| Ade Putri Tifani | 12.5% |
| Natasya Felisita Br Ginting | 12.5% |
| Jesika Filosovi Br P-A | 12.5% |
| Nabila Ramadhani Mujahidin | 12.5% |
| Annisa Salsabila | 12.5% |
| Willy Syifa Luthfia | 12.5% |
| Silvia | 12.5% |
