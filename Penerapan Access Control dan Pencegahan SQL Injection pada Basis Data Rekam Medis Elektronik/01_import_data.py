import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="rme_db"
)
cur = conn.cursor()

print("Membaca healthcare_dataset.csv ...")
df = pd.read_csv("healthcare_dataset.csv")
print(f"Total baris: {len(df)}")

# Kita import 5000 baris dulu supaya tidak terlalu lama
df = df.head(5000)

print("Mengimpor data ke MySQL ...")
for i, row in df.iterrows():
    # Insert doctor
    cur.execute("INSERT IGNORE INTO doctors (name) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM doctors WHERE name=%s)",
                (row['Doctor'], row['Doctor']))
    
    cur.execute("SELECT doctor_id FROM doctors WHERE name=%s LIMIT 1", (row['Doctor'],))
    doctor_id = cur.fetchone()[0]

    # Insert hospital
    cur.execute("INSERT IGNORE INTO hospitals (name, location) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM hospitals WHERE name=%s)",
                (row['Hospital'], 'Indonesia', row['Hospital']))
    cur.execute("SELECT hospital_id FROM hospitals WHERE name=%s LIMIT 1", (row['Hospital'],))
    hospital_id = cur.fetchone()[0]

    # Insert patient
    cur.execute("""
        INSERT INTO patients (name, age, gender, blood_type)
        VALUES (%s, %s, %s, %s)
    """, (row['Name'], int(row['Age']), row['Gender'], row['Blood Type']))
    patient_id = cur.lastrowid

    # Insert medical_record
    cur.execute("""
        INSERT INTO medical_records 
        (patient_id, doctor_id, hospital_id, admission_date, discharge_date, `condition`, admission_type, room_number, test_results)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        patient_id, doctor_id, hospital_id,
        row['Date of Admission'], row['Discharge Date'],
        row['Medical Condition'], row['Admission Type'],
        str(row['Room Number']), row['Test Results']
    ))
    record_id = cur.lastrowid

    # Insert billing
    cur.execute("""
        INSERT INTO billing (record_id, insurance_provider, billing_amount)
        VALUES (%s, %s, %s)
    """, (record_id, row['Insurance Provider'], float(row['Billing Amount'])))

    if (i+1) % 500 == 0:
        conn.commit()
        print(f"  {i+1} baris diimport...")

conn.commit()
cur.close()
conn.close()
print("Import selesai!")