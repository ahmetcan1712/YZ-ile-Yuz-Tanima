@echo off
echo [1/3] requirements.txt içindeki paketler yükleniyor...
pip install -r requirements.txt

echo [2/3] OpenCV çakışmalarını temizliyor...
pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python

echo [3/3] Doğru opencv-contrib-python yükleniyor...
pip install opencv-contrib-python==4.5.4.60

echo Tüm işlem tamamlandı. Artık uygulamanız çakışmasız çalışacaktır.
pause