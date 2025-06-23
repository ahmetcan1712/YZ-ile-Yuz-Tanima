import sqlite3
import numpy as np

DB_NAME = "yuzler.db"

def veritabani_baglan():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def kisi_sil(kullanici_adi):
    conn, cursor = veritabani_baglan()
    cursor.execute("DELETE FROM yuzler WHERE kullanici_adi = ?", (kullanici_adi,))
    conn.commit()
    conn.close()

def kullanici_var_mi(kullanici_adi):
    conn, cursor = veritabani_baglan()
    cursor.execute("SELECT COUNT(*) FROM yuzler WHERE kullanici_adi = ?", (kullanici_adi,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0

def vektor_ekle(isim, kullanici_adi, vektor):
    conn, cursor = veritabani_baglan()
    cursor.execute("INSERT INTO yuzler (isim, kullanici_adi, vektor) VALUES (?, ?, ?)",
                   (isim, kullanici_adi, vektor.tobytes()))
    conn.commit()
    conn.close()

def vektorleri_yukle():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT isim, vektor FROM yuzler")
    data = cursor.fetchall()
    isimler = []
    vektorler = []
    for isim, vektor_blob in data:
        isimler.append(isim)
        vektorler.append(np.frombuffer(vektor_blob, dtype=np.float64))
    conn.close()
    return isimler, np.array(vektorler)