import requests
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QSize
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
)
import base64

class ServerStatusWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip

    def run(self):
        try:
            # Using API v3
            url = f"https://api.mcsrvstat.us/3/{self.ip}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))

class ServerCard(QFrame):
    remove_requested = pyqtSignal(str) # Emits the IP to remove

    def __init__(self, ip, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.worker = None

        self.setObjectName("card")
        self.setStyleSheet("""
            QFrame#card {
                background-color: rgba(0, 0, 0, 0.4);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        self.init_ui()
        self.refresh()

    def contextMenuEvent(self, event):
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        remove_action = menu.addAction("Remove Server")
        refresh_action = menu.addAction("Refresh Status")

        action = menu.exec(event.globalPos())

        if action == remove_action:
            self.remove_requested.emit(self.ip)
        elif action == refresh_action:
            self.refresh()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(64, 64)
        self.icon_label.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 4px;")
        layout.addWidget(self.icon_label, 0, 0, 2, 1)

        # Info Layout
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        # Header Row: Hostname | Remove Button
        header_layout = QHBoxLayout()

        self.hostname_label = QLabel(self.ip)
        self.hostname_label.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        header_layout.addWidget(self.hostname_label)

        header_layout.addStretch(1)

        self.remove_button = QPushButton("✕")
        self.remove_button.setFixedSize(24, 24)
        self.remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_button.setToolTip("Remove Server")
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888;
                font-weight: bold;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #ff5555;
            }
        """)
        self.remove_button.clicked.connect(lambda: self.remove_requested.emit(self.ip))
        header_layout.addWidget(self.remove_button)

        info_layout.addLayout(header_layout)

        # Online Status & Players
        self.status_label = QLabel("Checking...")
        self.status_label.setStyleSheet("color: #cccccc;")
        info_layout.addWidget(self.status_label)

        # MOTD
        self.motd_label = QLabel()
        self.motd_label.setWordWrap(True)
        self.motd_label.setStyleSheet("color: #aaaaaa; font-style: italic; font-size: 11px;")
        self.motd_label.setMaximumHeight(40)
        info_layout.addWidget(self.motd_label)

        layout.addLayout(info_layout, 0, 1, 2, 1)

    def refresh(self):
        self.status_label.setText("Refreshing...")
        if self.worker and self.worker.isRunning():
            return

        self.worker = ServerStatusWorker(self.ip)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.worker.start()

    @pyqtSlot(dict)
    def on_success(self, data):
        online = data.get("online", False)

        if online:
            hostname = data.get("hostname", self.ip)
            # Prefer showing the friendly hostname if available, but keep IP in tooltip
            self.hostname_label.setText(hostname)
            self.hostname_label.setToolTip(self.ip)

            players = data.get("players", {})
            online_players = players.get("online", 0)
            max_players = players.get("max", 0)
            version = data.get("version", "Unknown")

            self.status_label.setText(f"🟢 Online  •  {online_players}/{max_players} Players  •  {version}")

            # MOTD
            motd = data.get("motd", {})
            clean_motd = motd.get("clean", [])
            self.motd_label.setText("\n".join(clean_motd) if clean_motd else "")

            # Icon
            icon_data = data.get("icon")
            if icon_data and icon_data.startswith("data:image/png;base64,"):
                try:
                    base64_data = icon_data.split(",")[1]
                    image_data = base64.b64decode(base64_data)
                    image = QImage.fromData(image_data)
                    pixmap = QPixmap.fromImage(image)
                    self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                except Exception as e:
                    print(f"Error loading icon: {e}")
                    self.icon_label.clear()
            else:
                 self.icon_label.clear()
        else:
            self.status_label.setText("🔴 Offline")
            self.motd_label.setText("Server could not be reached.")
            self.icon_label.clear()

    @pyqtSlot(str)
    def on_error(self, error_msg):
        self.status_label.setText("⚠️ Error")
        self.motd_label.setText(error_msg)
        self.icon_label.clear()

