import glob
import json
import os
import shutil
import sys
from PyQt6 import sip
import uuid
from PyQt6.QtCore import QThread, pyqtSlot, Qt, QTimer, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QRect
from PyQt6.QtGui import QColor, QCloseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizeGrip,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QStackedLayout,
)

from .constants import (
    APP_NAME,
    IMAGES_DIR,
    VERSIONS_CACHE_PATH,
    ICON_CACHE_DIR,
    MicrosoftInfo
)
from .mod_manager import ModsPage
from .stylesheet import STYLESHEET
from .workers import ImageDownloader, VersionFetcher, Worker
from .microsoft_auth import MicrosoftAuth
from .actions import setup_actions_and_menus
from .mod_browser import ModBrowserPage

from .config_manager import ConfigManager
from .launch_page import LaunchPage
from .settings_page import SettingsPage
from .background_widget import BackgroundWidget
from .console_window import ConsoleWindow
from .servers_page import ServersPage
from .skin_manager import SkinManagerPage
from .toast_manager import ToastManager
from .animated_widgets import NavIndicatorWidget
from .title_bar import TitleBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.worker_thread = None
        self.worker = None
        self.version_fetch_thread = None
        self.image_downloader_thread = None
        self.bg_timer = None
        self.minecraft_info: MicrosoftInfo | None = None
        self.current_background_style = ""
        self.last_version = None
        self.is_launching = False

        self.image_files = []
        self.current_image_index = 0

        self._nav_buttons: list[QPushButton] = []
        self._current_nav_button = None

        self.console_window = ConsoleWindow()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(900, 520)
        self.resize(1080, 660)

        # Frameless window with translucent background for rounded corners
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.microsoft_auth = MicrosoftAuth()
        self.microsoft_auth.login_success.connect(self.on_login_success)
        self.microsoft_auth.login_failed.connect(self.update_status)

        self.init_ui()

        self.toast_manager = ToastManager(self)

        self.load_settings()
        self.apply_styles()
        self.add_shadow_effects()
        self.populate_versions()
        self.init_background_images()
        self.load_microsoft_info()

        setup_actions_and_menus(self)
        # On macOS the menu bar is native (top of screen) and must stay visible
        # for CMD+Q and other system shortcuts. Hide it only on other platforms.
        if sys.platform != "darwin":
            self.menuBar().hide()

        self._setup_resize_grip()

        # Defer initial indicator position until layout is computed
        QTimer.singleShot(0, lambda: self._position_indicator_to(self.nav_launch_button))

    def show(self):
        super().show()
        self.setWindowOpacity(0.0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(450)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def _setup_resize_grip(self):
        self._size_grip = QSizeGrip(self)
        self._size_grip.setFixedSize(16, 16)
        self._reposition_grip()

    def _reposition_grip(self):
        if hasattr(self, '_size_grip'):
            self._size_grip.move(self.width() - 16, self.height() - 16)
            self._size_grip.raise_()

    def load_settings(self):
        last_username = self.config_manager.get("last_username", "")
        self.last_version = self.config_manager.get("last_version", "")
        if last_username:
            self.launch_page.username_input.setText(last_username)

    def init_ui(self):
        # Transparent root container
        main_container = QWidget()
        main_container.setObjectName("main_central_widget")
        self.setCentralWidget(main_container)

        root_layout = QVBoxLayout(main_container)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Background widget sits behind everything via QStackedLayout
        self.stack_layout = QStackedLayout()
        self.stack_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        stack_container = QWidget()
        stack_container.setLayout(self.stack_layout)
        root_layout.addWidget(stack_container)

        # Layer 0: Background
        self.background_widget = BackgroundWidget(self)
        self.stack_layout.addWidget(self.background_widget)

        # Layer 1: UI content
        ui_layer = QWidget()
        ui_layer.setObjectName("main_central_widget")
        self.stack_layout.addWidget(ui_layer)
        ui_layer.raise_()
        self.stack_layout.setCurrentWidget(ui_layer)

        # Small margin so the background image peeks around the rounded dark card
        ui_outer = QVBoxLayout(ui_layer)
        ui_outer.setContentsMargins(6, 6, 6, 6)
        ui_outer.setSpacing(0)

        # Rounded app frame — the single dark card over the background
        app_frame = QFrame()
        app_frame.setObjectName("app_outer_frame")
        ui_outer.addWidget(app_frame)

        app_frame_layout = QVBoxLayout(app_frame)
        app_frame_layout.setContentsMargins(0, 0, 0, 0)
        app_frame_layout.setSpacing(0)

        # Title bar
        self.title_bar = TitleBar(app_frame)
        app_frame_layout.addWidget(self.title_bar)

        # Inner area: sidebar + content
        inner_widget = QWidget()
        main_layout = QHBoxLayout(inner_widget)
        main_layout.setContentsMargins(10, 6, 10, 10)
        main_layout.setSpacing(10)
        app_frame_layout.addWidget(inner_widget)

        # ── Left Sidebar ──
        left_widget = QWidget()
        left_widget.setObjectName("left_title_container")
        left_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(2)
        left_layout.setContentsMargins(8, 8, 8, 8)

        # Title area
        title_frame = QFrame()
        title_frame.setObjectName("title_frame")
        title_frame_layout = QVBoxLayout(title_frame)
        title_frame_layout.setSpacing(0)
        title_frame_layout.setContentsMargins(10, 12, 10, 16)

        title_label = QLabel("PyMCL")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_frame_layout.addWidget(title_label)

        subtitle_label = QLabel("Python Minecraft Launcher")
        subtitle_label.setObjectName("subtitle_label")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_frame_layout.addWidget(subtitle_label)
        left_layout.addWidget(title_frame)

        # "NAVIGATION" section label
        nav_section_label = QLabel("NAVIGATION")
        nav_section_label.setObjectName("section_label")
        nav_section_label.setContentsMargins(18, 4, 0, 4)
        left_layout.addWidget(nav_section_label)

        # Sliding nav indicator (child of left_widget, not in layout)
        self.nav_indicator = NavIndicatorWidget(left_widget)
        self.nav_indicator.hide()

        # Nav buttons
        self.nav_launch_button = self._make_nav_button("🚀  Launch")
        self.nav_servers_button = self._make_nav_button("🌐  Servers")
        self.nav_skins_button = self._make_nav_button("🎨  Skins")
        self.nav_mods_button = self._make_nav_button("🧩  Mods")
        self.nav_browse_mods_button = self._make_nav_button("🔍  Browse Mods")
        self.nav_settings_button = self._make_nav_button("⚙️  Settings")
        self.nav_console_button = self._make_nav_button("🖥️  Console")
        self.nav_console_button.clicked.connect(self.show_console)

        for btn in [
            self.nav_launch_button,
            self.nav_servers_button,
            self.nav_skins_button,
            self.nav_mods_button,
            self.nav_browse_mods_button,
            self.nav_settings_button,
            self.nav_console_button,
        ]:
            left_layout.addWidget(btn)

        left_layout.addStretch(1)

        # Bottom: separator + version
        bottom_widget = QWidget()
        bottom_widget.setObjectName("sidebar_bottom")
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(6, 6, 6, 6)
        bottom_layout.setSpacing(4)

        separator = QFrame()
        separator.setObjectName("sidebar_separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        bottom_layout.addWidget(separator)

        version_label = QLabel("PyMCL  ·  v1.0")
        version_label.setObjectName("sidebar_version_label")
        bottom_layout.addWidget(version_label)

        left_layout.addWidget(bottom_widget)

        main_layout.addWidget(left_widget, 1)

        # ── Right Content ──
        content_frame = QFrame()
        content_frame.setObjectName("central_widget_frame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(content_frame, 3)

        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)

        self.launch_page = LaunchPage()
        self.settings_page = SettingsPage()
        self.settings_page.settings_saved.connect(self.reload_background_settings)
        self.settings_page.settings_saved.connect(lambda: self.toast_manager.show_toast("Settings have been saved.", "Settings Saved", "SUCCESS"))
        self.mods_page = ModsPage()
        self.mod_browser_page = ModBrowserPage()
        self.servers_page = ServersPage()
        self.skin_manager_page = SkinManagerPage()

        self.stacked_widget.addWidget(self.launch_page)       # 0
        self.stacked_widget.addWidget(self.servers_page)      # 1
        self.stacked_widget.addWidget(self.skin_manager_page) # 2
        self.stacked_widget.addWidget(self.mods_page)         # 3
        self.stacked_widget.addWidget(self.mod_browser_page)  # 4
        self.stacked_widget.addWidget(self.settings_page)     # 5

        self.nav_launch_button.clicked.connect(lambda: self.switch_page(0, self.nav_launch_button))
        self.nav_servers_button.clicked.connect(lambda: self.switch_page(1, self.nav_servers_button))
        self.nav_skins_button.clicked.connect(lambda: self.switch_page(2, self.nav_skins_button))
        self.nav_mods_button.clicked.connect(lambda: self.switch_page(3, self.nav_mods_button))
        self.nav_browse_mods_button.clicked.connect(lambda: self.switch_page(4, self.nav_browse_mods_button))
        self.nav_settings_button.clicked.connect(lambda: self.switch_page(5, self.nav_settings_button))

        self.launch_page.username_input.textChanged.connect(self.save_settings)
        self.launch_page.auth_method_combo.currentTextChanged.connect(self.update_auth_widgets)
        self.launch_page.microsoft_login_button.clicked.connect(self.start_microsoft_login)
        self.launch_page.launch_button.clicked.connect(self.start_launch)
        self.launch_page.mod_manager_button.clicked.connect(self.open_mod_manager)

        self.launch_page.version_combo.currentTextChanged.connect(self.mods_page.set_version)

        self.update_auth_widgets()

    def _make_nav_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("nav_button")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._nav_buttons.append(btn)
        return btn

    def _position_indicator_to(self, button: QPushButton):
        """Slide the nav indicator to the given button's position."""
        self._current_nav_button = button

        # Update active text color on all buttons
        for btn in self._nav_buttons:
            btn.setProperty("active", btn is button)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Map button rect into left_widget coordinate space
        btn_rect = button.geometry()
        inset = 2
        target = QRect(
            btn_rect.x() + inset,
            btn_rect.y(),
            btn_rect.width() - inset * 2,
            btn_rect.height(),
        )
        self.nav_indicator.slide_to(target)

        # Keep indicator behind buttons visually by raising buttons on top
        self.nav_indicator.raise_()
        for btn in self._nav_buttons:
            btn.raise_()

    def reload_background_settings(self):
        if self.bg_timer:
            self.bg_timer.stop()
        else:
            self.bg_timer = QTimer(self)
            self.bg_timer.timeout.connect(self.update_background_image)

        enable_slideshow = self.config_manager.get("enable_slideshow", True)
        if enable_slideshow and len(self.image_files) > 1:
            interval = self.config_manager.get("slideshow_interval", 30) * 1000
            self.bg_timer.start(interval)
        else:
            print("Background slideshow disabled or not enough images.")

    def switch_page(self, index, button):
        current_index = self.stacked_widget.currentIndex()
        if index == current_index:
            return

        if self.stacked_widget.widget(index) == self.mod_browser_page:
            version = self.launch_page.version_combo.currentText()
            mod_loader = self.launch_page.mod_loader_combo.currentText()

            loader_param = None
            if mod_loader == "Fabric":
                loader_param = "fabric"
            elif mod_loader == "Forge":
                loader_param = "forge"
            elif mod_loader == "NeoForge":
                loader_param = "neoforge"
            elif mod_loader == "Quilt":
                loader_param = "quilt"

            if version and version != "Loading versions...":
                self.mod_browser_page.set_launch_filters(version, loader_param)
            else:
                self.mod_browser_page.set_launch_filters(None, loader_param)

        # Move the sliding indicator
        self._position_indicator_to(button)

        # Animate the page transition
        self.slide_animation = self._create_slide_animation(index, current_index)
        self.slide_animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _create_slide_animation(self, new_index, old_index):
        width = self.stacked_widget.width()
        height = self.stacked_widget.height()
        offset = max(int(width * 0.28), 60)
        going_forward = new_index > old_index

        # Use snapshots (opaque QLabels) for both pages so the real widgets —
        # which QStackedLayout repositions at (0,0) — never interfere with
        # the animation geometry, and no transparent-widget overlap can occur.
        from PyQt6.QtWidgets import QLabel

        old_widget = self.stacked_widget.widget(old_index)
        new_widget = self.stacked_widget.widget(new_index)

        snap_old = QLabel(self.stacked_widget)
        snap_old.setPixmap(old_widget.grab())
        snap_old.setGeometry(0, 0, width, height)
        snap_old.show()
        snap_old.raise_()

        snap_new = QLabel(self.stacked_widget)
        snap_new.setPixmap(new_widget.grab())
        snap_new.setGeometry(offset if going_forward else -offset, 0, width, height)
        snap_new.show()
        snap_new.raise_()

        # Switch the real stacked widget while both snapshots are covering it.
        self.stacked_widget.setCurrentIndex(new_index)

        anim_old = QPropertyAnimation(snap_old, b"pos")
        anim_old.setDuration(280)
        anim_old.setStartValue(QPoint(0, 0))
        anim_old.setEndValue(QPoint(-offset if going_forward else offset, 0))
        anim_old.setEasingCurve(QEasingCurve.Type.InOutCubic)

        anim_new = QPropertyAnimation(snap_new, b"pos")
        anim_new.setDuration(280)
        anim_new.setStartValue(QPoint(offset if going_forward else -offset, 0))
        anim_new.setEndValue(QPoint(0, 0))
        anim_new.setEasingCurve(QEasingCurve.Type.OutCubic)

        anim_group = QParallelAnimationGroup()
        anim_group.addAnimation(anim_old)
        anim_group.addAnimation(anim_new)
        anim_group.finished.connect(snap_old.deleteLater)
        anim_group.finished.connect(snap_new.deleteLater)
        return anim_group

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'toast_manager'):
            self.toast_manager.reposition_toasts()
        if hasattr(self, '_current_nav_button') and self._current_nav_button:
            self._position_indicator_to(self._current_nav_button)
        self._reposition_grip()

    def update_auth_widgets(self):
        auth_method = self.launch_page.auth_method_combo.currentText()
        if auth_method == "Offline":
            self.launch_page.username_label.setVisible(True)
            self.launch_page.username_input.setVisible(True)
            self.launch_page.microsoft_login_button.setVisible(False)
        elif auth_method == "Microsoft":
            self.launch_page.username_label.setVisible(False)
            self.launch_page.username_input.setVisible(False)
            self.launch_page.microsoft_login_button.setVisible(True)

    def start_microsoft_login(self):
        self.microsoft_auth.start_login()

    def on_login_success(self, info: MicrosoftInfo):
        self.minecraft_info = info
        self.toast_manager.show_toast(f"Logged in as {info['username']}", "Login Successful", "SUCCESS")
        self.update_status(f"Logged in as {info['username']}")
        self.launch_page.microsoft_login_button.setText(f"Logged in as {info['username']}")
        self.skin_manager_page.set_microsoft_info(info)

    def load_microsoft_info(self):
        info = self.microsoft_auth.load_microsoft_info()
        if info:
            if self.microsoft_auth.is_token_expired():
                self.update_status("Refreshing token...")
                info = self.microsoft_auth.refresh_token()

            if info:
                self.minecraft_info = info
                self.update_status(f"Logged in as {info['username']}")
                self.launch_page.microsoft_login_button.setText(f"Logged in as {info['username']}")
                self.launch_page.auth_method_combo.setCurrentText("Microsoft")
                self.skin_manager_page.set_microsoft_info(info)
            else:
                self.update_status("Failed to refresh token. Please login again.")

    def apply_styles(self):
        self.setStyleSheet(STYLESHEET)

    def add_shadow_effects(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 8)
        self.findChild(QFrame, "central_widget_frame").setGraphicsEffect(shadow)

        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(20)
        title_shadow.setColor(QColor(0, 0, 0, 80))
        title_shadow.setOffset(0, 3)
        self.findChild(QFrame, "title_frame").setGraphicsEffect(title_shadow)

    def init_background_images(self):
        exts = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.mp4", "*.webm", "*.mkv", "*.avi"]
        self.image_files = []
        for ext in exts:
            self.image_files.extend(glob.glob(os.path.join(IMAGES_DIR, ext)))

        if not self.image_files:
            self.image_downloader_thread = ImageDownloader()
            self.image_downloader_thread.result.connect(self.on_image_downloaded)
            self.image_downloader_thread.start()
        else:
            self.update_background_image()

            if len(self.image_files) > 1:
                enable_slideshow = self.config_manager.get("enable_slideshow", True)
                if enable_slideshow:
                    interval = self.config_manager.get("slideshow_interval", 30) * 1000
                    self.bg_timer = QTimer(self)
                    self.bg_timer.timeout.connect(self.update_background_image)
                    self.bg_timer.start(interval)

    @pyqtSlot(bool, str)
    def on_image_downloaded(self, success, path):
        if success:
            self.image_files = [path]
            self.current_image_index = 0
            self.update_background_image()
        else:
            print(f"Failed to download background image: {path}")

    @pyqtSlot()
    def update_background_image(self):
        if not self.image_files:
            return

        path = self.image_files[self.current_image_index]

        if not os.path.exists(path):
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            return

        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)

        loop = self.config_manager.get("video_loop", True)
        mute = self.config_manager.get("video_mute", True)

        if path.lower().endswith((".mp4", ".webm", ".mkv", ".avi")):
            self.background_widget.set_video(path, loop, mute)
        elif path.lower().endswith('.gif'):
            self.background_widget.set_gif(path)
        else:
            self.background_widget.set_image(path)

    @pyqtSlot()
    def open_mod_manager(self):
        self.switch_page(3, self.nav_mods_button)

    def populate_versions(self):
        self.launch_page.status_label.setText("Loading versions...")
        self.launch_page.version_combo.setEnabled(False)

        cached_versions = self.load_versions_from_cache()
        if cached_versions:
            self.launch_page.version_combo.clear()
            self.launch_page.version_combo.addItems(cached_versions)

            if self.last_version and self.last_version in cached_versions:
                index = self.launch_page.version_combo.findText(self.last_version)
                if index != -1:
                    self.launch_page.version_combo.setCurrentIndex(index)

            self.launch_page.version_combo.setPlaceholderText("Select a version")
            self.launch_page.status_label.setText("Ready (versions fetched from cache)")
            self.launch_page.version_combo.setEnabled(True)
        else:
            self.launch_page.status_label.setText("Fetching version list...")
            self.launch_page.version_combo.setPlaceholderText("Loading...")

        self.version_fetch_thread = VersionFetcher()
        self.version_fetch_thread.result.connect(self._update_version_combo)
        self.version_fetch_thread.start()

    @pyqtSlot(list, bool, str)
    def _update_version_combo(self, versions, success, message):
        if success:
            current_versions = [
                self.launch_page.version_combo.itemText(i)
                for i in range(self.launch_page.version_combo.count())
            ]

            if current_versions != versions:
                current_selection = self.launch_page.version_combo.currentText()
                self.launch_page.version_combo.clear()
                self.launch_page.version_combo.addItems(versions)

                if current_selection and current_selection in versions:
                    index = self.launch_page.version_combo.findText(current_selection)
                    if index != -1:
                        self.launch_page.version_combo.setCurrentIndex(index)
                elif self.last_version and self.last_version in versions:
                    index = self.launch_page.version_combo.findText(self.last_version)
                    if index != -1:
                        self.launch_page.version_combo.setCurrentIndex(index)

                self.launch_page.status_label.setText("Versions updated")
            else:
                if not self.launch_page.status_label.text().startswith("Ready"):
                    self.launch_page.status_label.setText("Ready to launch")

            self.save_versions_to_cache(versions)
            self.launch_page.version_combo.setPlaceholderText("Select a version")
        else:
            if self.launch_page.version_combo.count() == 0:
                self.launch_page.version_combo.setPlaceholderText("Failed to load")
                self.launch_page.status_label.setText(message)

        self.launch_page.version_combo.setEnabled(True)

    def load_versions_from_cache(self):
        if not os.path.exists(VERSIONS_CACHE_PATH):
            return None
        try:
            with open(VERSIONS_CACHE_PATH, "r") as f:
                data = json.load(f)
                versions = data.get("release_versions", [])
                if versions:
                    return versions
        except Exception as e:
            print(f"Error loading version cache: {e}")
        return None

    def save_versions_to_cache(self, versions):
        try:
            with open(VERSIONS_CACHE_PATH, "w") as f:
                json.dump({"release_versions": versions}, f)
        except Exception as e:
            print(f"Error saving version cache: {e}")

    def save_settings(self):
        self.config_manager.set("last_username", self.launch_page.username_input.text().strip())
        self.config_manager.set("last_version", self.launch_page.version_combo.currentText())
        self.config_manager.save()

    @pyqtSlot()
    def show_console(self):
        self.console_window.show()
        self.console_window.raise_()
        self.console_window.activateWindow()

    @pyqtSlot()
    def start_launch(self):
        if self.is_launching:
            self.cancel_launch()
            return

        auth_method = self.launch_page.auth_method_combo.currentText()
        version = self.launch_page.version_combo.currentText()
        mod_loader_type = self.launch_page.mod_loader_combo.currentText()

        if not version or version == "Loading versions...":
            self.update_status("⚠️ Please select a version")
            return

        options = {
            "username": "",
            "uuid": "",
            "token": "",
            "executablePath": self.config_manager.get("java_executable"),
            "jvmArguments": self.config_manager.get("jvm_arguments", "").split(),
            "resolutionWidth": self.config_manager.get("resolution", {}).get("width"),
            "resolutionHeight": self.config_manager.get("resolution", {}).get("height"),
        }

        memory_gb = self.config_manager.get("memory_gb", 4)
        options["jvmArguments"].append(f"-Xmx{memory_gb}G")
        options["jvmArguments"].append(f"-Xms{memory_gb}G")

        if auth_method == "Offline":
            username = self.launch_page.username_input.text().strip()
            if not username:
                self.update_status("⚠️ Please enter a username")
                self.toast_manager.show_toast("Please enter a username to continue.", "Username Required", "WARNING")
                self.launch_page.username_input.shake()
                return
            options["username"] = username
            options["uuid"] = str(uuid.uuid4())
            self.save_settings()
        elif auth_method == "Microsoft":
            if not self.minecraft_info:
                self.update_status("⚠️ Please login with Microsoft")
                return
            options["username"] = self.minecraft_info["username"]
            options["uuid"] = self.minecraft_info["uuid"]
            options["token"] = self.minecraft_info["access_token"]
            self.save_settings()

        self.is_launching = True
        self.launch_page.launch_button.setText("❌ CANCEL LAUNCH")
        self.launch_page.launch_button.setProperty("class", "destructive")
        self.launch_page.launch_button.style().unpolish(self.launch_page.launch_button)
        self.launch_page.launch_button.style().polish(self.launch_page.launch_button)

        self.launch_page.status_label.setText("Starting worker thread...")
        self.launch_page.progress_bar.setRange(0, 100)
        self.launch_page.progress_bar.setValue(0)

        self.console_window.clear_logs()
        self.console_window.show()

        self.worker_thread = QThread()
        self.worker = Worker(version, options, mod_loader_type)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.log_output.connect(self.console_window.append_log)
        self.worker.telemetry_active.connect(lambda _, msg: self.toast_manager.show_toast(msg, "Privacy Shield Active", "SUCCESS"))
        self.worker.telemetry_step.connect(self.settings_page.set_telemetry_status)
        self.worker.finished.connect(self.on_launch_finished)

        self.worker.finished.connect(self.worker_thread.quit)

        self.worker_thread.start()

    @pyqtSlot(int, int)
    def update_progress(self, value, max_value):
        if max_value == 0:
            self.launch_page.progress_bar.setRange(0, 0)
            self.launch_page.progress_bar.setFormat("Loading...")
        else:
            self.launch_page.progress_bar.setRange(0, max_value)
            self.launch_page.progress_bar.setValue(value)
            self.launch_page.progress_bar.setFormat("%p%")

    @pyqtSlot(str)
    def update_status(self, message):
        self.launch_page.status_label.setText(message)

    @pyqtSlot(bool, str)
    def on_launch_finished(self, success, message):
        self.is_launching = False
        self.launch_page.launch_button.setProperty("class", "")
        self.launch_page.launch_button.style().unpolish(self.launch_page.launch_button)
        self.launch_page.launch_button.style().polish(self.launch_page.launch_button)

        self.launch_page.launch_button.setText("🚀 LAUNCH GAME")
        self.launch_page.status_label.setText(message)
        self.launch_page.progress_bar.setRange(0, 1)
        self.launch_page.progress_bar.setValue(1 if success else 0)
        self.launch_page.progress_bar.setFormat("%p%")

        if success:
            if "Game closed" in message:
                self.launch_page.progress_bar.setValue(0)
                self.launch_page.status_label.setText("✓ Ready to launch")
                self.toast_manager.show_toast("Minecraft session ended.", "Game Closed", "INFO")
            else:
                self.toast_manager.show_toast("Minecraft launched successfully!", "Launch Success", "SUCCESS")
        else:
            self.toast_manager.show_toast(message, "Launch Failed", "ERROR")

    def cancel_launch(self):
        if self.worker:
            self.worker.cancel()
            self.update_status("Cancelling launch...")
            self.launch_page.launch_button.setText("Stopping...")

    def clear_cache(self):
        try:
            if os.path.exists(ICON_CACHE_DIR):
                shutil.rmtree(ICON_CACHE_DIR)
                self.toast_manager.show_toast("The icon cache has been cleared.", "Cache Cleared", "SUCCESS")
            else:
                self.toast_manager.show_toast("No icon cache to clear.", "Cache Empty", "INFO")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not clear cache: {e}")

    @pyqtSlot()
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    @pyqtSlot()
    def show_about_dialog(self):
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME} - A custom Minecraft Launcher.\n\n"
            "Developed with Python and PyQt6.\n"
            "A Python Launcher for a Java game. We like to live dangerously."
        )

    def closeEvent(self, a0: QCloseEvent | None):
        if self.bg_timer:
            self.bg_timer.stop()

        if hasattr(self, 'worker_thread') and self.worker_thread and not sip.isdeleted(self.worker_thread) and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()

        if hasattr(self, 'version_fetch_thread') and self.version_fetch_thread and not sip.isdeleted(self.version_fetch_thread) and self.version_fetch_thread.isRunning():
            self.version_fetch_thread.quit()
            self.version_fetch_thread.wait()

        if hasattr(self, 'image_downloader_thread') and self.image_downloader_thread and not sip.isdeleted(self.image_downloader_thread) and self.image_downloader_thread.isRunning():
            self.image_downloader_thread.quit()
            self.image_downloader_thread.wait()

        if a0 is not None:
            a0.accept()
        else:
            super().closeEvent(a0)
