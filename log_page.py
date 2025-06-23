from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from log_utils import tum_loglari_al

class LogPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Tanınan Kişi Kayıtları")
        title.setObjectName("title")  # QSS ile uyumlu olsun
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.btn_refresh = QPushButton("Yenile")
        self.btn_back = QPushButton("Geri Dön")

        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_back)

        self.btn_refresh.clicked.connect(self.load_logs)
        self.btn_back.clicked.connect(lambda: self.parent.show_page(0))

        self.setLayout(layout)
        self.load_logs()

    def load_logs(self):
        logs = tum_loglari_al()
        self.table.setRowCount(len(logs))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["İsim", "Kullanıcı Adı", "Tarih-Saat", "Eşik Değeri", "Mesafe"])

        for row, log in enumerate(logs):
            for column, item in enumerate(log):
                if column == 4:  # Mesafe sütunu
                    item = f"{float(item):.2f}"
                self.table.setItem(row, column, QTableWidgetItem(str(item)))
