import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import cv2
import face_recognition
import faiss
import numpy as np

from db_utils import vektorleri_yukle
from detection import detect_faces
from tracking import TrackedFace, create_tracker
from camera import parlaklik_olc, dinamik_esik, histogram_esitleme_uygula
from user_management import KisiYonetimPage
from log_utils import log_ekle, veritabani_olustur
from log_page import LogPage


class CameraPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

        self.camera = cv2.VideoCapture()
        self.timer = self.parent.timer
        self.timer.timeout.connect(self.kamera_guncelle)

        self.tracked_faces = []
        self.frame_count = 0
        self.index = faiss.IndexFlatL2(128)
        self.isimler = []

    def setup_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Apartman Giriş Sistemi - Kamera")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.label = QLabel("Kamera Görüntüsü")
        self.label.setFixedSize(640, 480)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        stats_layout = QHBoxLayout()
        self.parlaklik_label = QLabel("Parlaklık: -")
        self.esik_label = QLabel("Eşik: -")
        self.kisi_sayisi = QLabel("Tanınan Kişi: 0")
        for label in [self.parlaklik_label, self.esik_label, self.kisi_sayisi]:
            stats_layout.addWidget(label)
        layout.addLayout(stats_layout)

        btn_layout = QHBoxLayout()
        self.btn_manage = QPushButton("Kişi Yönetimi")
        self.btn_manage.clicked.connect(lambda: self.parent.show_page(1))
        btn_layout.addWidget(self.btn_manage)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def kamera_baslat(self):
        self.isimler, vektorler = vektorleri_yukle()
        self.index.reset()
        if len(vektorler) > 0:
            self.index.add(vektorler)
        self.camera.open(0)
        if self.camera.isOpened():
            self.timer.start(30)

    def kamera_durdur(self):
        self.timer.stop()
        if self.camera.isOpened():
            self.camera.release()
        self.label.clear()
        self.label.setText("Kamera Görüntüsü")

    def kamera_guncelle(self):
        ret, frame = self.camera.read()
        if not ret:
            return

        parlaklik = parlaklik_olc(frame)
        esik = dinamik_esik(parlaklik)
        frame = histogram_esitleme_uygula(frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.frame_count % 50 == 0:
            boxes = detect_faces(frame_rgb)
            self.tracked_faces = []
            for (x1, y1, x2, y2) in boxes:
                top, right, bottom, left = int(y1), int(x2), int(y2), int(x1)
                bbox = (left, top, right - left, bottom - top)
                encodings = face_recognition.face_encodings(frame_rgb, [(top, right, bottom, left)], model='large')
                if not encodings:
                    continue
                vektor = encodings[0].astype('float32').reshape(1, -1)
                mesafeler, indeksler = self.index.search(vektor, 1)

                if len(self.isimler) == 0 or mesafeler[0][0] >= esik:
                    isim = "Taninmadi"
                else:
                    isim = self.isimler[indeksler[0][0]]
                    log_ekle(isim, isim, esik, float(mesafeler[0][0]))

                tracker = create_tracker(frame, bbox)
                self.tracked_faces.append(TrackedFace(tracker, isim))

        taninan_kisi = 0
        yeni_tracked_faces = []
        for tf in self.tracked_faces:
            success, bbox = tf.tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, tf.name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                yeni_tracked_faces.append(tf)
                if tf.name != "Taninmadi":
                    taninan_kisi += 1

        self.tracked_faces = yeni_tracked_faces
        self.parlaklik_label.setText(f"Parlaklık: {int(parlaklik)}")
        self.esik_label.setText(f"Eşik: {esik:.2f}")
        self.kisi_sayisi.setText(f"Tanınan Kişi: {taninan_kisi}")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qt_image))
        self.frame_count += 1

    def showEvent(self, event):
        self.kamera_baslat()

    def hideEvent(self, event):
        self.kamera_durdur()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apartman Giriş Sistemi")
        self.setGeometry(100, 100, 800, 600)
        self.timer = QTimer()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.stacked_widget = QStackedWidget()
        self.camera_page = CameraPage(self)
        self.kisi_yonetim_page = KisiYonetimPage(self)
        self.stacked_widget.addWidget(self.camera_page)
        self.stacked_widget.addWidget(self.kisi_yonetim_page)
        self.log_page = LogPage(self)
        self.stacked_widget.addWidget(self.log_page)
        layout.addWidget(self.stacked_widget)

        self.btn_logs = QPushButton("Kayıtlar")
        self.btn_logs.clicked.connect(lambda: self.show_page(2))
        layout.addWidget(self.btn_logs)

    def show_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
