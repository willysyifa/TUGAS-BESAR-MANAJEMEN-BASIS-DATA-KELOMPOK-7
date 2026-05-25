import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from middleware import detect_sqli

print("=" * 60)
print("SKENARIO C: EVALUASI DETEKSI SQL INJECTION")
print("=" * 60)

df = pd.read_csv("sql_dataset.csv")
print(f"Total query di dataset: {len(df)}")

# Sesuaikan nama kolom dengan dataset yang kamu download
# Biasanya kolom bernama 'Query' dan 'Label'
print(f"Kolom: {df.columns.tolist()}")

y_true = []
y_pred = []

for _, row in df.iterrows():
    query = str(row['Query'])   # ganti jika nama kolom berbeda
    label = int(row['Label'])   # 1=berbahaya, 0=aman

    is_sqli, _ = detect_sqli(query)
    predicted = 1 if is_sqli else 0

    y_true.append(label)
    y_pred.append(predicted)

print("\n--- Confusion Matrix ---")
cm = confusion_matrix(y_true, y_pred)
print(f"True Negative  (aman, terdeteksi aman)     : {cm[0][0]}")
print(f"False Positive (aman, salah dianggap SQLi) : {cm[0][1]}")
print(f"False Negative (SQLi, lolos tidak terdeteksi): {cm[1][0]}")
print(f"True Positive  (SQLi, berhasil diblokir)   : {cm[1][1]}")

print("\n--- Classification Report ---")
print(classification_report(y_true, y_pred, target_names=["Aman", "Berbahaya"]))

total_sqli = sum(1 for l in y_true if l == 1)
detected = cm[1][1]
print(f"\nDetection Rate : {detected}/{total_sqli} = {detected/total_sqli*100:.2f}%")