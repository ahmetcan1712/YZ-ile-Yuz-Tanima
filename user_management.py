from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QHBoxLayout, QFileDialog, QMessageBox, QListWidgetItem
from db_utils import kisi_sil, vektor_ekle, kullanici_var_mi
import face_recognition
import numpy as np
from PyQt5.QtCore import Qt

class KisiYonetimPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Kişi Yönetimi")
        layout.addWidget(title)

        self.list_widget = QListWidget()
        self.refresh_user_list()
        layout.addWidget(self.list_widget)

        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.username_input = QLineEdit()

        self.photo_label = QLabel("Seçilen Fotoğraf: Henüz seçilmedi")
        self.photo_button = QPushButton("Fotoğraf Seç")
        self.photo_button.clicked.connect(self.select_photo)
        self.selected_photo = None

        form_layout.addWidget(QLabel("İsim:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Kullanıcı Adı:"))
        form_layout.addWidget(self.username_input)

        layout.addWidget(self.photo_label)
        layout.addLayout(form_layout)
        layout.addWidget(self.photo_button)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Kişi Ekle")
        self.btn_delete = QPushButton("Seçili Kişiyi Sil")
        self.btn_back = QPushButton("Kameraya Dön")

        self.btn_add.clicked.connect(self.kisi_ekle)
        self.btn_delete.clicked.connect(self.kisi_sil)
        self.btn_back.clicked.connect(lambda: self.parent.show_page(0))

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_back)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def select_photo(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Fotoğraf Seç", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_photo = file_path
            self.photo_label.setText(f"Seçilen Fotoğraf: {file_path.split('/')[-1]}")

    def kisi_ekle(self):
        isim = self.name_input.text()
        kullanici_adi = self.username_input.text()
        foto = self.selected_photo
        if not isim or not kullanici_adi or not foto:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun ve fotoğraf seçin.")
            return
        if kullanici_var_mi(kullanici_adi):
            QMessageBox.warning(self, "Uyarı", "Bu kullanıcı adı zaten var. Lütfen farklı bir kullanıcı adı girin.")
            return
        image = face_recognition.load_image_file(foto)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            QMessageBox.warning(self, "Uyarı", "Yüz bulunamadı.")
            return
        vektor_ekle(isim, kullanici_adi, encodings[0])
        QMessageBox.information(self, "Başarılı", f"{isim} eklendi.")
        self.refresh_user_list()

    def kisi_sil(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek kişiyi seçin.")
            return
        kullanici_adi = selected_item.data(Qt.UserRole)
        kisi_sil(kullanici_adi)
        QMessageBox.information(self, "Başarılı", f"{selected_item.text()} silindi.")
        self.refresh_user_list()

    def refresh_user_list(self):
        from db_utils import veritabani_baglan
        conn, cursor = veritabani_baglan()
        cursor.execute("SELECT isim, kullanici_adi FROM yuzler")
        data = cursor.fetchall()
        self.list_widget.clear()
        for isim, kullanici_adi in data:
            item = QListWidgetItem(isim)
            item.setData(Qt.UserRole, kullanici_adi)
            self.list_widget.addItem(item)
        conn.close()