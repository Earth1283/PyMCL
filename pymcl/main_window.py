import glob
import json
import os
import shutil
import sys
from PyQt6 import sip
import uuid
from PyQt6.QtCore import QThread, pyqtSlot, Qt, QTimer, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint
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

# New imports
from .config_manager import ConfigManager
from .launch_page import LaunchPage
from .settings_page import SettingsPage
from .background_widget import BackgroundWidget
from .console_window import ConsoleWindow
from .servers_page import ServersPage
from .skin_manager import SkinManagerPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.worker_thread = None
        self.worker = None
        self.version_fetch_thread = None
        self.version_fetcher = None
        self.image_downloader_thread = None
        self.image_downloader = None
        self.bg_timer = None
        self.minecraft_info: MicrosoftInfo | None = None
        self.current_background_style = ""
        self.last_version = None
        self.is_launching = False

        self.image_files = []
        self.current_image_index = 0
        
        # New console window
        self.console_window = ConsoleWindow()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(900, 500)
        self.resize(1050, 650)

        self.microsoft_auth = MicrosoftAuth()
        self.microsoft_auth.login_success.connect(self.on_login_success)
        self.microsoft_auth.login_failed.connect(self.update_status)

        self.init_ui()
        self.load_settings()
        self.apply_styles()
        self.add_shadow_effects()
        self.populate_versions()
        self.init_background_images()
        self.load_microsoft_info()

        setup_actions_and_menus(self)

    def show(self):
        super().show()
        self.setWindowOpacity(0.0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def load_settings(self):
        last_username = self.config_manager.get("last_username", "")
        self.last_version = self.config_manager.get("last_version", "")
        if last_username:
            self.launch_page.username_input.setText(last_username)

    def init_ui(self):
        # Container for everything using Stacked Layout for background
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        self.stack_layout = QStackedLayout(main_container)
        self.stack_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        
        # Layer 1: Background Widget
        self.background_widget = BackgroundWidget(self)
        self.stack_layout.addWidget(self.background_widget)
        
        # Layer 2: UI Content
        central_widget = QWidget()
        central_widget.setObjectName("main_central_widget")
        self.stack_layout.addWidget(central_widget)
        
        # Ensure UI is on top
        central_widget.raise_()
        self.stack_layout.setCurrentWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Left navigation Scroll Area
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll.setStyleSheet("background: transparent;") # Transparent background
        
        # Left navigation container
        left_widget = QWidget()
        left_widget.setObjectName("left_title_container")
        # Ensure the widget itself has transparent bg if styled otherwise in stylesheet
        left_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(5)
        left_layout.setContentsMargins(10, 10, 10, 10)

        title_frame = QFrame()
        title_frame.setObjectName("title_frame")
        title_frame_layout = QVBoxLayout(title_frame)
        title_frame_layout.setSpacing(0)
        title_frame_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(APP_NAME)
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_frame_layout.addWidget(title_label)

        subtitle_label = QLabel("Python Minecraft Launcher")
        subtitle_label.setObjectName("subtitle_label")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_frame_layout.addWidget(subtitle_label)
        left_layout.addWidget(title_frame)

        self.nav_launch_button = QPushButton("Launch")
        self.nav_launch_button.setObjectName("nav_button_active")
        self.nav_launch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        left_layout.addWidget(self.nav_launch_button)

        self.nav_servers_button = QPushButton("Servers")
        self.nav_servers_button.setObjectName("nav_button")
        self.nav_servers_button.setCursor(Qt.CursorShape.PointingHandCursor)
        left_layout.addWidget(self.nav_servers_button)

        self.nav_skins_button = QPushButton("Skins")
        self.nav_skins_button.setObjectName("nav_button")
        self.nav_skins_button.setCursor(Qt.CursorShape.PointingHandCursor)
        left_layout.addWidget(self.nav_skins_button)

        self.nav_mods_button = QPushButton("Mods")
        self.nav_mods_button.setObjectName("nav_button")
        self.nav_mods_button.setCursor(Qt.CursorShape.PointingHandCursor)
        left_layout.addWidget(self.nav_mods_button)

        self.nav_browse_mods_button = QPushButton("Browse Mods")
        self.nav_browse_mods_button.setObjectName("nav_button")
        self.nav_browse_mods_button.setCursor(Qt.CursorShape.PointingHandCursor)
        left_layout.addWidget(self.nav_browse_mods_button)

        self.nav_settings_button = QPushButton("Settings")
        self.nav_settings_button.setObjectName("nav_button")
        self.nav_settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        left_layout.addWidget(self.nav_settings_button)

        self.nav_console_button = QPushButton("Console")
        self.nav_console_button.setObjectName("nav_button")
        self.nav_console_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nav_console_button.clicked.connect(self.show_console)
        left_layout.addWidget(self.nav_console_button)

        left_layout.addStretch(1)
        
        left_scroll.setWidget(left_widget)
        main_layout.addWidget(left_scroll, 2)

        # Right content
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
        self.mods_page = ModsPage()
        self.mod_browser_page = ModBrowserPage()
        self.servers_page = ServersPage()
        self.skin_manager_page = SkinManagerPage()

        self.stacked_widget.addWidget(self.launch_page)       # Index 0
        self.stacked_widget.addWidget(self.servers_page)      # Index 1
        self.stacked_widget.addWidget(self.skin_manager_page) # Index 2
        self.stacked_widget.addWidget(self.mods_page)         # Index 3
        self.stacked_widget.addWidget(self.mod_browser_page)  # Index 4
        self.stacked_widget.addWidget(self.settings_page)     # Index 5

        self.nav_launch_button.clicked.connect(lambda: self.switch_page(0, self.nav_launch_button))
        self.nav_servers_button.clicked.connect(lambda: self.switch_page(1, self.nav_servers_button))
        self.nav_skins_button.clicked.connect(lambda: self.switch_page(2, self.nav_skins_button))
        self.nav_mods_button.clicked.connect(lambda: self.switch_page(3, self.nav_mods_button))
        self.nav_browse_mods_button.clicked.connect(lambda: self.switch_page(4, self.nav_browse_mods_button))
        self.nav_settings_button.clicked.connect(lambda: self.switch_page(5, self.nav_settings_button))

        # Connect signals from launch page to main window slots
        self.launch_page.username_input.textChanged.connect(self.save_settings)
        self.launch_page.auth_method_combo.currentTextChanged.connect(self.update_auth_widgets)
        self.launch_page.microsoft_login_button.clicked.connect(self.start_microsoft_login)
        self.launch_page.launch_button.clicked.connect(self.start_launch)
        self.launch_page.mod_manager_button.clicked.connect(self.open_mod_manager)
        
        # Connect version change to mods page
        self.launch_page.version_combo.currentTextChanged.connect(self.mods_page.set_version)

        self.update_auth_widgets()

    def reload_background_settings(self):
        print("Reloading background settings...")
        if self.bg_timer:
            self.bg_timer.stop()
        else:
             self.bg_timer = QTimer(self)
             self.bg_timer.timeout.connect(self.update_background_image)

        enable_slideshow = self.config_manager.get("enable_slideshow", True)
        if enable_slideshow and len(self.image_files) > 1:
            interval = self.config_manager.get("slideshow_interval", 30) * 1000
            self.bg_timer.start(interval)
            print(f"Background timer started with interval: {interval}ms")
        else:
             print("Background slideshow disabled or not enough images.")

    def switch_page(self, index, button):
        current_index = self.stacked_widget.currentIndex()
        if index == current_index:
            return

        # Pass launch options to mod browser
        if self.stacked_widget.widget(index) == self.mod_browser_page:
            version = self.launch_page.version_combo.currentText()
            mod_loader = self.launch_page.mod_loader_combo.currentText()
            loader_param = None
            if mod_loader == "Fabric":
                loader_param = "fabric"
            # Add conditions for other loaders if Modrinth API supports them
            # For now, only Fabric is directly mapped
            self.mod_browser_page.set_launch_filters(version, loader_param)

        # Update nav button styles
        for btn in [self.nav_launch_button, self.nav_mods_button, self.nav_browse_mods_button, self.nav_settings_button, self.nav_servers_button, self.nav_skins_button]:
            btn.setObjectName("nav_button")
        button.setObjectName("nav_button_active")
        self.apply_styles()

        # Animation
        self.slide_animation = self._create_slide_animation(index, current_index)
        self.slide_animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _create_slide_animation(self, new_index, old_index):
        width = self.stacked_widget.width()

        # New widget to slide in
        new_widget = self.stacked_widget.widget(new_index)
        new_widget.setGeometry(0, 0, width, self.stacked_widget.height())
        new_widget.move(width if new_index > old_index else -width, 0)
        new_widget.show()
        new_widget.raise_()

        anim_new = QPropertyAnimation(new_widget, b"pos")
        anim_new.setDuration(300)
        anim_new.setEndValue(self.stacked_widget.rect().topLeft())
        anim_new.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Old widget to slide out
        old_widget = self.stacked_widget.widget(old_index)
        anim_old = QPropertyAnimation(old_widget, b"pos")
        anim_old.setDuration(300)
        anim_old.setEndValue(QPoint(width if new_index < old_index else -width, 0))
        anim_old.setEasingCurve(QEasingCurve.Type.OutCubic)

        anim_group = QParallelAnimationGroup()
        anim_group.addAnimation(anim_new)
        anim_group.addAnimation(anim_old)

        anim_group.finished.connect(lambda: self.on_animation_finished(new_index, old_widget))
        return anim_group

    def on_animation_finished(self, new_index, old_widget):
        self.stacked_widget.setCurrentIndex(new_index)
        old_widget.hide()
        old_widget.move(0, 0)

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
        # We no longer apply background image to stylesheet
        self.setStyleSheet(STYLESHEET)

    def add_shadow_effects(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.findChild(QFrame, "central_widget_frame").setGraphicsEffect(shadow)

        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(20)
        title_shadow.setColor(QColor(0, 0, 0, 80))
        title_shadow.setOffset(0, 3)
        self.findChild(QFrame, "title_frame").setGraphicsEffect(title_shadow)

    def init_background_images(self):
        print("Initializing background media...")
        exts = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.mp4", "*.webm", "*.mkv", "*.avi"]
        self.image_files = []
        for ext in exts:
            self.image_files.extend(glob.glob(os.path.join(IMAGES_DIR, ext)))

        if not self.image_files:
            print("No background media found. Downloading default image.")
            self.image_downloader_thread = QThread()
            self.image_downloader = ImageDownloader()
            self.image_downloader.moveToThread(self.image_downloader_thread)

            self.image_downloader_thread.started.connect(self.image_downloader.run)
            self.image_downloader.finished.connect(self.on_image_downloaded)

            self.image_downloader.finished.connect(self.image_downloader_thread.quit)
            self.image_downloader.finished.connect(self.image_downloader.deleteLater)
            self.image_downloader_thread.finished.connect(
                self.image_downloader_thread.deleteLater
            )

            self.image_downloader_thread.start()
        else:
            print(f"Found {len(self.image_files)} media files.")
            self.update_background_image()

            if len(self.image_files) > 1:
                enable_slideshow = self.config_manager.get("enable_slideshow", True)
                if enable_slideshow:
                    interval = self.config_manager.get("slideshow_interval", 30) * 1000
                    print(f"Starting background timer with interval {interval}ms...")
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
            print(f"Media file not found: {path}")
            # Try next one
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            return

        self.current_image_index = (self.current_image_index + 1) % len(
            self.image_files
        )

        print(f"Setting background to: {path}")

        # Load settings for loop/mute
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
        self.switch_page(1, self.nav_mods_button)

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

        self.version_fetch_thread = QThread()
        self.version_fetcher = VersionFetcher()
        self.version_fetcher.moveToThread(self.version_fetch_thread)

        self.version_fetch_thread.started.connect(self.version_fetcher.run)
        self.version_fetcher.finished.connect(self._update_version_combo)

        self.version_fetcher.finished.connect(self.version_fetch_thread.quit)
        self.version_fetcher.finished.connect(self.version_fetcher.deleteLater)
        self.version_fetch_thread.finished.connect(
            self.version_fetch_thread.deleteLater
        )

        self.version_fetch_thread.start()

    @pyqtSlot(list, bool, str)
    def _update_version_combo(self, versions, success, message):
        if success:
            current_versions = [
                self.launch_page.version_combo.itemText(i)
                for i in range(self.launch_page.version_combo.count())
            ]

            if current_versions != versions:
                print("Updating version list from network...")
                current_selection = self.launch_page.version_combo.currentText()
                self.launch_page.version_combo.clear()
                self.launch_page.version_combo.addItems(versions)

                # Restore previous selection or load last played version
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
                print("Cached versions are up-to-date.")
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
                    print(f"Loaded {len(versions)} versions from cache.")
                    return versions
        except Exception as e:
            print(f"Error loading version cache: {e}")
            return None
        return None

    def save_versions_to_cache(self, versions):
        try:
            with open(VERSIONS_CACHE_PATH, "w") as f:
                json.dump({"release_versions": versions}, f)
            print("Saved fresh versions to cache.")
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
        modifiers = QApplication.keyboardModifiers()
        if self.is_launching:
            if modifiers & Qt.KeyboardModifier.ShiftModifier:
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
        self.launch_page.launch_button.setText("⏳ LAUNCHING...")
        self.launch_page.status_label.setText("Starting worker thread...")
        self.launch_page.progress_bar.setRange(0, 100)
        self.launch_page.progress_bar.setValue(0)
        
        # Clear console and show it
        self.console_window.clear_logs()
        self.console_window.show()

        self.worker_thread = QThread()
        self.worker = Worker(version, options, mod_loader_type)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.log_output.connect(self.console_window.append_log) # Connect logs
        self.worker.finished.connect(self.on_launch_finished)

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

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

        if success and "Game closed" in message:
            self.launch_page.progress_bar.setValue(0)
            self.launch_page.status_label.setText("✓ Ready to launch")

    def cancel_launch(self):
        if self.worker:
            self.worker.cancel()
            self.update_status("Cancelling launch...")
            self.launch_page.launch_button.setText("Stopping...")

    def keyPressEvent(self, event):
        if self.is_launching and event.key() == Qt.Key.Key_Shift:
            self.launch_page.launch_button.setText("❌ CANCEL LAUNCH")
            self.launch_page.launch_button.setProperty("class", "destructive")
            self.launch_page.launch_button.style().unpolish(self.launch_page.launch_button)
            self.launch_page.launch_button.style().polish(self.launch_page.launch_button)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if self.is_launching and event.key() == Qt.Key.Key_Shift:
            self.launch_page.launch_button.setText("⏳ LAUNCHING...")
            self.launch_page.launch_button.setProperty("class", "")
            self.launch_page.launch_button.style().unpolish(self.launch_page.launch_button)
            self.launch_page.launch_button.style().polish(self.launch_page.launch_button)
        super().keyReleaseEvent(event)

    def clear_cache(self):
        try:
            if os.path.exists(ICON_CACHE_DIR):
                shutil.rmtree(ICON_CACHE_DIR)
                QMessageBox.information(self, "Cache Cleared", "The icon cache has been cleared.")
            else:
                QMessageBox.information(self, "Cache Cleared", "No icon cache to clear.")
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
