import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import os

os.makedirs("hasil", exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'figure.dpi': 150
})

BIRU    = '#378ADD'
HIJAU   = '#1D9E75'
ORANYE  = '#D85A30'
MERAH   = '#E24B4A'
KUNING  = '#EF9F27'
ABU     = '#888780'

# ============================================================
# GAMBAR 1 — DASHBOARD UTAMA (2x2 panel)
# ============================================================
fig = plt.figure(figsize=(16, 12))
fig.patch.set_facecolor('#FAFAFA')
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# --- Panel 1: TPS vs Concurrent Users ---
ax1 = fig.add_subplot(gs[0, 0])
users      = [10, 50, 100, 200]
tps_sistem = [54, 355, 427, 526]

bars = ax1.bar(users, tps_sistem, color=BIRU, width=15, zorder=3, edgecolor='white', linewidth=0.5)
ax1.set_xlabel('Concurrent Users', fontsize=11)
ax1.set_ylabel('TPS (transaksi/detik)', fontsize=11)
ax1.set_title('Throughput (TPS) vs Beban Pengguna', fontsize=12, fontweight='bold', pad=12)
ax1.set_xticks(users)
ax1.set_facecolor('#F8F8F8')
for bar, val in zip(bars, tps_sistem):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
             str(val), ha='center', va='bottom', fontsize=10, fontweight='bold', color=BIRU)

# --- Panel 2: Latency vs Concurrent Users ---
ax2 = fig.add_subplot(gs[0, 1])
lat_avg = [176, 36, 34, 34]
lat_max = [184, 53, 50, 69]

ax2.plot(users, lat_avg, 'o-', color=HIJAU, linewidth=2.5, markersize=8,
         label='Avg latency', zorder=3)
ax2.plot(users, lat_max, 's--', color=ORANYE, linewidth=2, markersize=7,
         label='Max latency', zorder=3)
ax2.fill_between(users, lat_avg, lat_max, alpha=0.12, color=HIJAU)

for x, y in zip(users, lat_avg):
    ax2.annotate(f'{y}ms', (x, y), textcoords='offset points',
                 xytext=(0, 10), ha='center', fontsize=9, color=HIJAU, fontweight='bold')
for x, y in zip(users, lat_max):
    ax2.annotate(f'{y}ms', (x, y), textcoords='offset points',
                 xytext=(0, -16), ha='center', fontsize=9, color=ORANYE)

ax2.set_xlabel('Concurrent Users', fontsize=11)
ax2.set_ylabel('Latency (ms)', fontsize=11)
ax2.set_title('Latency vs Beban Pengguna', fontsize=12, fontweight='bold', pad=12)
ax2.set_xticks(users)
ax2.legend(fontsize=10, framealpha=0.7)
ax2.set_facecolor('#F8F8F8')

# --- Panel 3: Confusion Matrix ---
ax3 = fig.add_subplot(gs[1, 0])
cm_data   = np.array([[18826, 711], [4023, 7359]])
cm_labels = [['True Negative\n(Aman → Diloloskan)', 'False Positive\n(Aman → Diblokir)'],
             ['False Negative\n(SQLi → Lolos)', 'True Positive\n(SQLi → Diblokir)']]
colors_cm = [['#EAF3DE', '#FAEEDA'], ['#FAEEDA', '#EAF3DE']]
txt_colors = [['#27500A', '#633806'], ['#633806', '#27500A']]

ax3.set_xlim(0, 2)
ax3.set_ylim(0, 2)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title('Confusion Matrix — Deteksi SQL Injection', fontsize=12, fontweight='bold', pad=12)

for i in range(2):
    for j in range(2):
        rect = mpatches.FancyBboxPatch(
            (j + 0.05, 1 - i + 0.05), 0.9, 0.9,
            boxstyle="round,pad=0.02",
            facecolor=colors_cm[i][j], edgecolor='white', linewidth=2
        )
        ax3.add_patch(rect)
        ax3.text(j + 0.5, 1 - i + 0.62,
                 f'{cm_data[i][j]:,}',
                 ha='center', va='center', fontsize=18,
                 fontweight='bold', color=txt_colors[i][j])
        ax3.text(j + 0.5, 1 - i + 0.28,
                 cm_labels[i][j],
                 ha='center', va='center', fontsize=8.5,
                 color=txt_colors[i][j], linespacing=1.4)

ax3.text(0.5, 2.08, 'Prediksi: Aman', ha='center', fontsize=10, color=ABU, fontweight='bold')
ax3.text(1.5, 2.08, 'Prediksi: Berbahaya', ha='center', fontsize=10, color=ABU, fontweight='bold')
ax3.text(-0.15, 1.5, 'Aktual:\nAman', ha='center', va='center', fontsize=10,
         color=ABU, fontweight='bold', rotation=90)
ax3.text(-0.15, 0.5, 'Aktual:\nBerbahaya', ha='center', va='center', fontsize=10,
         color=ABU, fontweight='bold', rotation=90)

# --- Panel 4: Metrik Klasifikasi ---
ax4 = fig.add_subplot(gs[1, 1])
kelas    = ['Aman', 'Berbahaya']
precision = [0.82, 0.91]
recall    = [0.96, 0.65]
f1        = [0.89, 0.76]

x    = np.arange(len(kelas))
w    = 0.25
b1   = ax4.bar(x - w, precision, w, label='Precision', color=BIRU,   zorder=3, edgecolor='white')
b2   = ax4.bar(x,     recall,    w, label='Recall',    color=HIJAU,  zorder=3, edgecolor='white')
b3   = ax4.bar(x + w, f1,        w, label='F1-score',  color=ORANYE, zorder=3, edgecolor='white')

for bars in [b1, b2, b3]:
    for bar in bars:
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{bar.get_height():.2f}',
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

ax4.set_xticks(x)
ax4.set_xticklabels(kelas, fontsize=11)
ax4.set_ylabel('Skor', fontsize=11)
ax4.set_ylim(0, 1.1)
ax4.set_title('Metrik Klasifikasi per Kelas', fontsize=12, fontweight='bold', pad=12)
ax4.legend(fontsize=10, framealpha=0.7)
ax4.set_facecolor('#F8F8F8')
ax4.axhline(y=0.85, color=MERAH, linestyle=':', linewidth=1.5, alpha=0.7, label='Target H1 (85%)')
ax4.text(1.55, 0.86, 'Target H1 (85%)', fontsize=8, color=MERAH, alpha=0.8)

fig.suptitle('Dashboard Hasil Eksperimen — Keamanan Basis Data RME\nKelompok 7 | IF25-40405 Manajemen Basis Data',
             fontsize=14, fontweight='bold', y=0.98, color='#2C2C2A')

plt.savefig('hasil/dashboard_utama.png', bbox_inches='tight', dpi=150, facecolor='#FAFAFA')
plt.close()
print("Gambar 1 disimpan: hasil/dashboard_utama.png")


# ============================================================
# GAMBAR 2 — HASIL UJI RBAC
# ============================================================
fig2, ax = plt.subplots(figsize=(10, 5))
fig2.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')
ax.axis('off')
ax.set_title('Hasil Pengujian RBAC — Akses Lintas Batas\nKelompok 7 | IF25-40405 Manajemen Basis Data',
             fontsize=13, fontweight='bold', pad=15, color='#2C2C2A')

rbac_data = [
    ('perawat_01', 'perawat',       'DELETE FROM medical_records',              'BLOCKED',  '#FCEBEB', '#A32D2D'),
    ('pasien_01',  'pasien',        'INSERT INTO medical_records',              'BLOCKED',  '#FCEBEB', '#A32D2D'),
    ('keuangan_01','staf_keuangan', "UPDATE patients SET name='hacked'",        'BLOCKED',  '#FCEBEB', '#A32D2D'),
    ('dokter_01',  'dokter',        'SELECT * FROM patients WHERE patient_id=1','ALLOWED',  '#EAF3DE', '#27500A'),
    ('admin_01',   'admin',         'DELETE FROM audit_log WHERE log_id=1',     'ALLOWED',  '#EAF3DE', '#27500A'),
]

headers = ['Username', 'Role', 'Query', 'Status']
col_w   = [0.15, 0.15, 0.50, 0.12]
col_x   = [0.02, 0.17, 0.32, 0.85]

for ci, (h, cx) in enumerate(zip(headers, col_x)):
    ax.text(cx, 0.92, h, fontsize=10, fontweight='bold', color=ABU,
            transform=ax.transAxes)

ax.plot([0.01, 0.99], [0.88, 0.88], color='#D3D1C7', linewidth=1,
        transform=ax.transAxes)

row_h = 0.13
for ri, (uname, role, query, status, bg, fg) in enumerate(rbac_data):
    y = 0.82 - ri * row_h
    bg_rect = mpatches.FancyBboxPatch(
        (0.01, y - 0.04), 0.98, row_h - 0.01,
        boxstyle="round,pad=0.005",
        facecolor=bg if status == 'BLOCKED' else '#F8FDF4',
        edgecolor='#D3D1C7', linewidth=0.5,
        transform=ax.transAxes, clip_on=False
    )
    ax.add_patch(bg_rect)
    ax.text(col_x[0], y + 0.02, uname,  fontsize=9.5, transform=ax.transAxes, color='#2C2C2A')
    ax.text(col_x[1], y + 0.02, role,   fontsize=9.5, transform=ax.transAxes, color='#444441', style='italic')
    ax.text(col_x[2], y + 0.02, query,  fontsize=8.5, transform=ax.transAxes,
            color='#444441', family='monospace')
    status_rect = mpatches.FancyBboxPatch(
        (col_x[3] - 0.01, y - 0.01), 0.13, 0.07,
        boxstyle="round,pad=0.01",
        facecolor=bg, edgecolor=fg, linewidth=1,
        transform=ax.transAxes, clip_on=False
    )
    ax.add_patch(status_rect)
    ax.text(col_x[3] + 0.055, y + 0.025, status, fontsize=9, fontweight='bold',
            color=fg, transform=ax.transAxes, ha='center', va='center')

ax.text(0.99, 0.02, 'Akurasi RBAC: 5/5 = 100% ✓',
        fontsize=10, fontweight='bold', color=HIJAU,
        transform=ax.transAxes, ha='right')

plt.savefig('hasil/grafik_rbac.png', bbox_inches='tight', dpi=150, facecolor='#FAFAFA')
plt.close()
print("Gambar 2 disimpan: hasil/grafik_rbac.png")


# ============================================================
# GAMBAR 3 — PERBANDINGAN 3 SISTEM (ESTIMASI BASELINE)
# ============================================================
fig3, axes = plt.subplots(1, 2, figsize=(13, 5))
fig3.patch.set_facecolor('#FAFAFA')

sistem  = ['Baseline A\n(Tanpa Keamanan)', 'Baseline B\n(RBAC Saja)', 'Sistem Usulan\n(RBAC+SQLi+Log)']
warna   = [ABU, KUNING, BIRU]

# estimasi baseline berdasarkan overhead theory (10-25% per layer)
tps_200  = [620, 570, 526]
lat_200  = [28,  31,  38]

ax_tps, ax_lat = axes
ax_tps.set_facecolor('#F8F8F8')
ax_lat.set_facecolor('#F8F8F8')

bars_tps = ax_tps.bar(sistem, tps_200, color=warna, width=0.4,
                       zorder=3, edgecolor='white', linewidth=0.8)
for bar, val in zip(bars_tps, tps_200):
    ax_tps.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                str(val), ha='center', fontsize=11, fontweight='bold')
ax_tps.set_ylabel('TPS (transaksi/detik)', fontsize=11)
ax_tps.set_title('Perbandingan Throughput (200 Users)', fontsize=12, fontweight='bold')
ax_tps.tick_params(axis='x', labelsize=9)

bars_lat = ax_lat.bar(sistem, lat_200, color=warna, width=0.4,
                       zorder=3, edgecolor='white', linewidth=0.8)
for bar, val in zip(bars_lat, lat_200):
    ax_lat.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{val}ms', ha='center', fontsize=11, fontweight='bold')
ax_lat.set_ylabel('Avg Latency (ms)', fontsize=11)
ax_lat.set_title('Perbandingan Latency (200 Users)', fontsize=12, fontweight='bold')
ax_lat.tick_params(axis='x', labelsize=9)

legend_patches = [
    mpatches.Patch(color=ABU,    label='Baseline A — tanpa keamanan (estimasi)'),
    mpatches.Patch(color=KUNING, label='Baseline B — RBAC saja (estimasi)'),
    mpatches.Patch(color=BIRU,   label='Sistem usulan — data aktual eksperimen'),
]
fig3.legend(handles=legend_patches, loc='lower center', ncol=3,
            fontsize=9, framealpha=0.7, bbox_to_anchor=(0.5, -0.05))

fig3.suptitle('Perbandingan Performa 3 Konfigurasi Sistem\nKelompok 7 | IF25-40405 Manajemen Basis Data',
              fontsize=13, fontweight='bold', y=1.02, color='#2C2C2A')

plt.tight_layout()
plt.savefig('hasil/grafik_perbandingan_sistem.png', bbox_inches='tight',
            dpi=150, facecolor='#FAFAFA')
plt.close()
print("Gambar 3 disimpan: hasil/grafik_perbandingan_sistem.png")


# ============================================================
# GAMBAR 4 — AUDIT LOG SUMMARY
# ============================================================
fig4, axes4 = plt.subplots(1, 2, figsize=(12, 5))
fig4.patch.set_facecolor('#FAFAFA')

ax_pie, ax_bar = axes4
ax_pie.set_facecolor('#FAFAFA')
ax_bar.set_facecolor('#F8F8F8')

status_labels = ['ALLOWED', 'BLOCKED\n(RBAC)', 'SQLI_BLOCKED']
status_vals   = [16, 3, 4]
status_colors = [HIJAU, KUNING, MERAH]
explode       = (0, 0.05, 0.08)

wedges, texts, autotexts = ax_pie.pie(
    status_vals, labels=status_labels, colors=status_colors,
    autopct='%1.0f%%', startangle=90, explode=explode,
    textprops={'fontsize': 10},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
for at in autotexts:
    at.set_fontweight('bold')
    at.set_fontsize(11)
ax_pie.set_title('Distribusi Status Audit Log', fontsize=12, fontweight='bold')

aktivitas = ['Import data\n(5000 records)', 'Uji keamanan\n(Skenario A)', 'Uji performa\n(Skenario B)', 'Uji SQLi\n(Skenario C)']
total_log  = [5000, 9, 10, 0]
warna_bar  = [BIRU, ORANYE, HIJAU, ABU]

bars4 = ax_bar.barh(aktivitas, total_log, color=warna_bar,
                     height=0.5, zorder=3, edgecolor='white')
for bar, val in zip(bars4, total_log):
    if val > 0:
        ax_bar.text(val + 30, bar.get_y() + bar.get_height()/2,
                    str(val), va='center', fontsize=10, fontweight='bold')
ax_bar.set_xlabel('Jumlah aktivitas tercatat', fontsize=11)
ax_bar.set_title('Aktivitas per Fase Eksperimen', fontsize=12, fontweight='bold')
ax_bar.set_xlim(0, 5600)

fig4.suptitle('Analisis Audit Log — Kelompok 7\nIF25-40405 Manajemen Basis Data',
              fontsize=13, fontweight='bold', y=1.02, color='#2C2C2A')

plt.tight_layout()
plt.savefig('hasil/grafik_audit_log.png', bbox_inches='tight',
            dpi=150, facecolor='#FAFAFA')
plt.close()
print("Gambar 4 disimpan: hasil/grafik_audit_log.png")


print("\n" + "="*55)
print("Semua visualisasi berhasil dibuat!")
print("Cek folder: hasil/")
print("  - dashboard_utama.png        → Gambar 3 paper")
print("  - grafik_rbac.png            → Gambar 4 paper")
print("  - grafik_perbandingan_sistem.png → Gambar 5 paper")
print("  - grafik_audit_log.png       → Gambar 7 paper")
print("="*55)