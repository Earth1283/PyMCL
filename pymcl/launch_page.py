import uuid
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QProgressBar,
    QScrollArea,
)

class LaunchPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("content_scroll_area")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.auth_method_label = QLabel("AUTHENTICATION")
        self.auth_method_label.setObjectName("section_label")
        layout.addWidget(self.auth_method_label)

        layout.addSpacing(5)

        self.auth_method_combo = QComboBox()
        self.auth_method_combo.addItems(["Offline", "Microsoft"])
        self.auth_method_combo.setMinimumHeight(55)
        layout.addWidget(self.auth_method_combo)

        layout.addSpacing(15)

        self.username_label = QLabel("USERNAME")
        self.username_label.setObjectName("section_label")
        layout.addWidget(self.username_label)

        layout.addSpacing(5)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setText(f"Player{uuid.uuid4().hex[:6]}")
        self.username_input.setMinimumHeight(55)
        layout.addWidget(self.username_input)

        self.microsoft_login_button = QPushButton("Login with Microsoft")
        self.microsoft_login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.microsoft_login_button.setMinimumHeight(55)
        layout.addWidget(self.microsoft_login_button)

        layout.addSpacing(15)

        version_label = QLabel("MINECRAFT VERSION")
        version_label.setObjectName("section_label")
        layout.addWidget(version_label)

        layout.addSpacing(5)

        self.version_combo = QComboBox()
        self.version_combo.setPlaceholderText("Loading versions...")
        self.version_combo.setMinimumHeight(55)
        layout.addWidget(self.version_combo)

        layout.addSpacing(15)

        mod_layout = QHBoxLayout()
        mod_layout.setSpacing(15)

        mod_loader_label = QLabel("MOD LOADER")
        mod_loader_label.setObjectName("section_label")
        mod_layout.addWidget(mod_loader_label, 0, Qt.AlignmentFlag.AlignVCenter)

        self.mod_loader_combo = QComboBox()
        self.mod_loader_combo.addItems(["Vanilla", "Fabric", "Forge", "NeoForge", "Quilt"])
        self.mod_loader_combo.setMinimumHeight(55)
        mod_layout.addWidget(self.mod_loader_combo)

        mod_layout.addStretch(1)

        self.mod_manager_button = QPushButton("Manage Mods")
        self.mod_manager_button.setObjectName("secondary_button")
        self.mod_manager_button.setCursor(Qt.CursorShape.PointingHandCursor)
        mod_layout.addWidget(self.mod_manager_button)

        layout.addLayout(mod_layout)

        layout.addSpacing(15)

        self.launch_button = QPushButton("🚀 LAUNCH GAME")
        self.launch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.launch_button.setMinimumHeight(55)
        layout.addWidget(self.launch_button)

        layout.addSpacing(10)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setMinimumHeight(32)
        layout.addWidget(self.progress_bar)

        layout.addSpacing(5)

        self.status_label = QLabel("Ready to launch")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch(1)

        scroll_area.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(scroll_area)
