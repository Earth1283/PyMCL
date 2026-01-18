import requests
import base64
import json
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QBuffer, QByteArray
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame,
    QScrollArea
)
from .config_manager import ConfigManager

class SkinFetcher(QThread):
    finished = pyqtSignal(QPixmap, bool) # pixmap, is_slim

    def __init__(self, uuid):
        super().__init__()
        self.uuid = uuid

    def run(self):
        try:
            # Get profile
            url = f"https://sessionserver.mojang.com/session/minecraft/profile/{self.uuid}"
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()

            # Decode texture property
            properties = data.get("properties", [])
            for prop in properties:
                if prop.get("name") == "textures":
                    value = base64.b64decode(prop.get("value")).decode("utf-8")
                    textures = json.loads(value).get("textures", {})
                    skin = textures.get("SKIN", {})
                    skin_url = skin.get("url")
                    metadata = skin.get("metadata", {})
                    is_slim = metadata.get("model") == "slim"

                    if skin_url:
                        img_resp = requests.get(skin_url)
                        img_resp.raise_for_status()
                        img = QImage.fromData(img_resp.content)
                        self.finished.emit(QPixmap.fromImage(img), is_slim)
                        return

            self.finished.emit(QPixmap(), False)
        except Exception as e:
            print(f"Skin fetch error: {e}")
            self.finished.emit(QPixmap(), False)

class SkinUploader(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, token, file_path, variant):
        super().__init__()
        self.token = token
        self.file_path = file_path
        self.variant = variant # "classic" or "slim"

    def run(self):
        try:
            url = "https://api.minecraftservices.com/minecraft/profile/skins"
            headers = {"Authorization": f"Bearer {self.token}"}

            with open(self.file_path, "rb") as f:
                files = {
                    "file": f,
                    "variant": (None, self.variant)
                }
                resp = requests.post(url, headers=headers, files=files)

            if resp.status_code == 200:
                self.finished.emit(True, "Skin uploaded successfully!")
            else:
                try:
                    err = resp.json().get("errorMessage", resp.text)
                except:
                    err = resp.text
                self.finished.emit(False, f"Upload failed: {err}")

        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class SkinPreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 400)
        self.raw_skin = None
        self.is_slim = False
        self.scale_factor = 4

    def set_skin(self, pixmap, is_slim):
        self.raw_skin = pixmap
        self.is_slim = is_slim
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False) # Keep pixel look

        if not self.raw_skin:
            # Draw placeholder text centered
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Skin Loaded")
            return

        # Basic 2D Front View Mapping
        # Head: 8,8 (8x8)
        # Body: 20,20 (8x12)
        # Arms: 44,20 (4x12) - Note: Alex/Slim is 3x12
        # Legs: 4,20 (4x12)

        # Scaling
        s = 16 # Draw scale

        # Center X
        cx = self.width() // 2
        cy = 50

        # Helper to draw rect from skin to screen
        def draw_part(sx, sy, w, h, dx, dy):
            part = self.raw_skin.copy(sx, sy, w, h).scaled(w*s, h*s, Qt.AspectRatioMode.IgnoreAspectRatio)
            painter.drawPixmap(dx, dy, part)

        # Draw Head
        draw_part(8, 8, 8, 8, cx - 4*s, cy)
        # Draw Hat layer (second layer)
        draw_part(40, 8, 8, 8, cx - 4*s, cy)

        # Draw Body
        draw_part(20, 20, 8, 12, cx - 4*s, cy + 8*s)
        # Jacket layer
        draw_part(20, 36, 8, 12, cx - 4*s, cy + 8*s)

        arm_w = 3 if self.is_slim else 4

        # Right Arm (Viewer's Left) - Actually mapped from Right Arm texture usually 44,20
        # For simplicity in 2D view we often just show one side or mirror.
        draw_part(44, 20, arm_w, 12, cx - 4*s - arm_w*s, cy + 8*s)

        # Left Arm (Viewer's Right)
        # If 64x64 skin (modern), left arm is at 36,52
        if self.raw_skin.height() == 64:
             draw_part(36, 52, arm_w, 12, cx + 4*s, cy + 8*s)
        else:
             # Old skin format, flip right arm? Or just draw same
             draw_part(44, 20, arm_w, 12, cx + 4*s, cy + 8*s)

        # Right Leg (Viewer's Left) - 4,20
        draw_part(4, 20, 4, 12, cx - 4*s, cy + 20*s)

        # Left Leg
        if self.raw_skin.height() == 64:
            draw_part(20, 52, 4, 12, cx, cy + 20*s)
        else:
            draw_part(4, 20, 4, 12, cx, cy + 20*s)


class SkinManagerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.minecraft_info = None
        self.uploader = None
        self.fetcher = None

        self.init_ui()

    def set_microsoft_info(self, info):
        self.minecraft_info = info
        if info:
            self.status_label.setText(f"Logged in as: {info.get('username')}")
            self.refresh_skin()
        else:
            self.status_label.setText("Please login via Microsoft first.")
            self.preview.set_skin(None, False)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("SKIN MANAGER")
        header.setObjectName("section_label")
        layout.addWidget(header)

        self.status_label = QLabel("Waiting for login...")
        self.status_label.setStyleSheet("color: #aaa;")
        layout.addWidget(self.status_label)

        # Content Layout (Preview Left, Controls Right)
        content_layout = QHBoxLayout()

        # Preview Area
        preview_container = QWidget()
        preview_container.setStyleSheet("background-color: rgba(0,0,0,0.3); border-radius: 10px;")
        preview_vbox = QVBoxLayout(preview_container)

        self.preview = SkinPreviewWidget()
        preview_vbox.addWidget(self.preview, 0, Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(preview_container)

        # Controls Area
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(15)

        lbl = QLabel("Upload New Skin")
        lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
        controls_layout.addWidget(lbl)

        self.variant_btn = QPushButton("Model: Classic (Steve)")
        self.variant_btn.setCheckable(True)
        self.variant_btn.clicked.connect(self.toggle_variant)
        self.variant_btn.setMinimumHeight(45)
        self.variant_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        controls_layout.addWidget(self.variant_btn)

        upload_btn = QPushButton("Select & Upload Skin")
        upload_btn.setObjectName("secondary_button")
        upload_btn.setMinimumHeight(45)
        upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_btn.clicked.connect(self.upload_skin)
        controls_layout.addWidget(upload_btn)

        refresh_btn = QPushButton("Refresh Current Skin")
        refresh_btn.setMinimumHeight(45)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_skin)
        controls_layout.addWidget(refresh_btn)

        controls_layout.addStretch(1)

        content_layout.addLayout(controls_layout)
        layout.addLayout(content_layout)

    def toggle_variant(self):
        if self.variant_btn.isChecked():
            self.variant_btn.setText("Model: Slim (Alex)")
        else:
            self.variant_btn.setText("Model: Classic (Steve)")

    def refresh_skin(self):
        if not self.minecraft_info:
            return

        uuid = self.minecraft_info.get("uuid")
        if not uuid:
            return

        self.status_label.setText("Fetching skin...")
        self.fetcher = SkinFetcher(uuid)
        self.fetcher.finished.connect(self.on_skin_fetched)
        self.fetcher.start()

    @pyqtSlot(QPixmap, bool)
    def on_skin_fetched(self, pixmap, is_slim):
        if not pixmap.isNull():
            self.preview.set_skin(pixmap, is_slim)
            self.status_label.setText("Skin loaded.")
        else:
            self.status_label.setText("Failed to load skin.")

    def upload_skin(self):
        if not self.minecraft_info:
            QMessageBox.warning(self, "Auth Required", "Please login with Microsoft to change your skin.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select Skin File", "", "Images (*.png)")
        if not file_path:
            return

        variant = "slim" if self.variant_btn.isChecked() else "classic"
        token = self.minecraft_info.get("access_token")

        self.status_label.setText("Uploading skin...")
        self.uploader = SkinUploader(token, file_path, variant)
        self.uploader.finished.connect(self.on_upload_finished)
        self.uploader.start()

    @pyqtSlot(bool, str)
    def on_upload_finished(self, success, msg):
        self.status_label.setText(msg)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.refresh_skin()
        else:
            QMessageBox.critical(self, "Error", msg)
