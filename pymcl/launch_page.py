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

from .animated_widgets import AnimatedButton, AnimatedInput

class LaunchPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("content_scroll_area")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        # Card 1: Authentication & Profile
        auth_card = QWidget()
        auth_card.setObjectName("card_container")
        auth_layout = QVBoxLayout(auth_card)
        auth_layout.setContentsMargins(24, 24, 24, 24)
        auth_layout.setSpacing(16)

        self.auth_method_label = QLabel("AUTHENTICATION")
        self.auth_method_label.setObjectName("section_label")
        auth_layout.addWidget(self.auth_method_label)

        self.auth_method_combo = QComboBox()
        self.auth_method_combo.addItems(["Offline", "Microsoft"])
        self.auth_method_combo.setMinimumHeight(55)
        self.auth_method_combo.setToolTip("Choose 'Microsoft' for online play or 'Offline' for local play.")
        auth_layout.addWidget(self.auth_method_combo)

        auth_layout.addSpacing(8)

        self.username_label = QLabel("USERNAME")
        self.username_label.setObjectName("section_label")
        auth_layout.addWidget(self.username_label)

        self.username_input = AnimatedInput()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setText(f"Player{uuid.uuid4().hex[:6]}")
        self.username_input.setMinimumHeight(55)
        self.username_input.setToolTip("Enter the username you want to use in-game (Offline mode only).")
        auth_layout.addWidget(self.username_input)

        self.microsoft_login_button = AnimatedButton("Login with Microsoft")
        self.microsoft_login_button.setMinimumHeight(55)
        self.microsoft_login_button.setToolTip("Sign in with your Microsoft account to play online.")
        auth_layout.addWidget(self.microsoft_login_button)

        layout.addWidget(auth_card)

        # Card 2: Game Configuration
        config_card = QWidget()
        config_card.setObjectName("card_container")
        config_layout = QVBoxLayout(config_card)
        config_layout.setContentsMargins(24, 24, 24, 24)
        config_layout.setSpacing(16)

        version_label = QLabel("MINECRAFT VERSION")
        version_label.setObjectName("section_label")
        config_layout.addWidget(version_label)

        self.version_combo = QComboBox()
        self.version_combo.setPlaceholderText("Loading versions...")
        self.version_combo.setMinimumHeight(55)
        self.version_combo.setToolTip("Select the Minecraft version to launch.")
        config_layout.addWidget(self.version_combo)

        config_layout.addSpacing(8)

        mod_layout = QHBoxLayout()
        mod_layout.setSpacing(16)

        mod_loader_container = QWidget()
        mod_loader_layout = QVBoxLayout(mod_loader_container)
        mod_loader_layout.setContentsMargins(0, 0, 0, 0)
        mod_loader_layout.setSpacing(6)
        
        mod_loader_label = QLabel("MOD LOADER")
        mod_loader_label.setObjectName("section_label")
        mod_loader_layout.addWidget(mod_loader_label)

        self.mod_loader_combo = QComboBox()
        self.mod_loader_combo.addItems(["Vanilla", "Fabric", "Forge", "NeoForge", "Quilt"])
        self.mod_loader_combo.setMinimumHeight(55)
        self.mod_loader_combo.setToolTip("Choose the mod loader (e.g., Fabric, Forge) or use Vanilla.")
        mod_loader_layout.addWidget(self.mod_loader_combo)
        
        mod_layout.addWidget(mod_loader_container, 2)

        mod_btn_container = QWidget()
        mod_btn_layout = QVBoxLayout(mod_btn_container)
        mod_btn_layout.setContentsMargins(0, 0, 0, 0)
        mod_btn_layout.setSpacing(6)
        
        mod_btn_label = QLabel(" ")  # Spacer for alignment
        mod_btn_label.setObjectName("section_label")
        mod_btn_layout.addWidget(mod_btn_label)

        self.mod_manager_button = AnimatedButton("Manage Mods", is_secondary=True)
        self.mod_manager_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mod_manager_button.setMinimumHeight(55)
        self.mod_manager_button.setToolTip("Open the Mod Manager to add or remove mods.")
        mod_btn_layout.addWidget(self.mod_manager_button)
        
        mod_layout.addWidget(mod_btn_container, 1)

        config_layout.addLayout(mod_layout)

        layout.addWidget(config_card)

        # Launch Area Bottom
        layout.addStretch(1)

        launch_area = QWidget()
        launch_layout = QVBoxLayout(launch_area)
        launch_layout.setContentsMargins(0, 0, 0, 0)
        launch_layout.setSpacing(12)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setMinimumHeight(16)
        # Hide progress bar until we need it, or keep it visible but very thin
        launch_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready to launch")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        launch_layout.addWidget(self.status_label)

        self.launch_button = AnimatedButton("🚀 LAUNCH GAME")
        self.launch_button.setMinimumHeight(70) # Taller primary CTA
        self.launch_button.setStyleSheet("font-size: 18px; font-weight: 800; letter-spacing: 1px;") # Overrides will be added for scale
        self.launch_button.setToolTip("Start Minecraft with the selected configuration.")
        launch_layout.addWidget(self.launch_button)

        layout.addWidget(launch_area)

        scroll_area.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(scroll_area)
