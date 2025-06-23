# Apartman Giriş Sistemi — Yüz Tanıma Tabanlı Gerçek Zamanlı Kimlik Doğrulama
📄 README.md



Bu proje, apartman ve site gibi toplu yaşam alanlarında yetkisiz girişleri engellemek amacıyla geliştirilmiş, **yüz tanıma tabanlı gerçek zamanlı bir kimlik doğrulama ve takip sistemi** prototipidir.  
Açık kaynak teknolojiler kullanılarak düşük maliyetli, hızlı ve kullanıcı dostu bir çözüm sunulması hedeflenmiştir.

---

## 🚀 **Kurulum Adımları**

### 1️⃣ Python Sanal Ortam Oluşturma

Proje Python **3.9** sürümü ile test edilmiştir.  
Öncelikle bilgisayarınıza Python 3.9 kurulu olduğundan emin olun.

Ardından proje klasöründe bir sanal ortam oluşturun:

```bash
# Windows PowerShell / CMD:
python -m venv venv

# Sanal ortamı aktifleştirme:
venv\Scripts\activate

2️⃣ Gerekli Kütüphaneleri Kurma
Sanal ortam aktifken, proje dizininde bulunan install_requirements.bat dosyasını çalıştırarak ihtiyaç duyulan tüm Python kütüphaneleri otomatik olarak kurulacaktır.


# Windows Komut Satırında:
install_requirements.bat



⚙️ Uygulamayı Çalıştırma
Kurulum tamamlandıktan sonra, sanal ortamınız aktifken aşağıdaki komutu çalıştırarak sistemi başlatabilirsiniz:

python main.py

Uygulama başlatıldığında:

Kamera görüntüsü alınır.

YOLO algoritmasıyla yüz tespiti yapılır.

Tespit edilen yüzler Face Recognition ile vektörleştirilir.

FAISS kullanılarak veritabanı ile karşılaştırılır.

Tanınan yüzler CSRT Tracker ile takip edilir.

Giriş kayıtları SQLite veritabanına kaydedilir.

PyQt5 arayüzü üzerinden kullanıcı işlemleri yapılabilir.
