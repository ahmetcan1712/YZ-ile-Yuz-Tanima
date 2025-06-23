import sqlite3
from datetime import datetime

LOG_DB = "logs.db"

def veritabani_olustur():
    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT,
            kullanici_adi TEXT,
            tarih_saat TEXT,
            esik_degeri REAL,
            mesafe REAL
        )
    """)
    conn.commit()
    conn.close()

def log_ekle(isim, kullanici_adi, esik_degeri, mesafe):
    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (isim, kullanici_adi, tarih_saat, esik_degeri, mesafe)
        VALUES (?, ?, ?, ?, ?)
    """, (isim, kullanici_adi, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), esik_degeri, mesafe))
    conn.commit()
    conn.close()

def tum_loglari_al():
    conn = sqlite3.connect(LOG_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT isim, kullanici_adi, tarih_saat, esik_degeri, mesafe FROM logs ORDER BY tarih_saat DESC")
    data = cursor.fetchall()
    conn.close()
    return data
