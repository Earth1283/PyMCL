import os
import sys
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QSlider,
    QCheckBox,
    QMessageBox,
)

from .constants import MINECRAFT_DIR
from .config_manager import ConfigManager

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # --- General Tab ---
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(15)
        
        # Mods directory setting
        mods_dir_label = QLabel("MODS DIRECTORY")
        mods_dir_label.setObjectName("section_label")
        general_layout.addWidget(mods_dir_label)

        mods_dir_layout = QHBoxLayout()
        self.mods_dir_input = QLineEdit()
        self.mods_dir_input.setPlaceholderText("Enter mods directory path")
        self.mods_dir_input.setMinimumHeight(55)
        mods_dir_layout.addWidget(self.mods_dir_input)

        mods_dir_browse_button = QPushButton("Browse")
        mods_dir_browse_button.setObjectName("secondary_button")
        mods_dir_browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        mods_dir_browse_button.clicked.connect(lambda: self.browse_directory(self.mods_dir_input))
        mods_dir_layout.addWidget(mods_dir_browse_button)
        general_layout.addLayout(mods_dir_layout)

        # Images directory setting
        images_dir_label = QLabel("BACKGROUND IMAGES DIRECTORY")
        images_dir_label.setObjectName("section_label")
        general_layout.addWidget(images_dir_label)

        images_dir_layout = QHBoxLayout()
        self.images_dir_input = QLineEdit()
        self.images_dir_input.setPlaceholderText("Enter images directory path")
        self.images_dir_input.setMinimumHeight(55)
        images_dir_layout.addWidget(self.images_dir_input)

        images_dir_browse_button = QPushButton("Browse")
        images_dir_browse_button.setObjectName("secondary_button")
        images_dir_browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        images_dir_browse_button.clicked.connect(lambda: self.browse_directory(self.images_dir_input))
        images_dir_layout.addWidget(images_dir_browse_button)
        general_layout.addLayout(images_dir_layout)
        
        # Open Data Folder Button
        open_data_dir_button = QPushButton("Open Data Folder")
        open_data_dir_button.setObjectName("secondary_button")
        open_data_dir_button.setCursor(Qt.CursorShape.PointingHandCursor)
        open_data_dir_button.clicked.connect(self.open_data_directory)
        general_layout.addWidget(open_data_dir_button)
        
        general_layout.addStretch(1)
        self.tabs.addTab(general_tab, "General")


        # --- Java & Performance Tab ---
        java_tab = QWidget()
        java_layout = QVBoxLayout(java_tab)
        java_layout.setContentsMargins(20, 20, 20, 20)
        java_layout.setSpacing(15)

        # Java executable setting
        java_executable_label = QLabel("JAVA EXECUTABLE (OPTIONAL)")
        java_executable_label.setObjectName("section_label")
        java_layout.addWidget(java_executable_label)

        java_executable_layout = QHBoxLayout()
        self.java_executable_input = QLineEdit()
        self.java_executable_input.setPlaceholderText("Enter Java executable path")
        self.java_executable_input.setMinimumHeight(55)
        java_executable_layout.addWidget(self.java_executable_input)

        java_executable_browse_button = QPushButton("Browse")
        java_executable_browse_button.setObjectName("secondary_button")
        java_executable_browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        java_executable_browse_button.clicked.connect(lambda: self.browse_file(self.java_executable_input))
        java_executable_layout.addWidget(java_executable_browse_button)
        java_layout.addLayout(java_executable_layout)

        # JVM arguments setting
        jvm_args_label = QLabel("JVM ARGUMENTS (ADVANCED)")
        jvm_args_label.setObjectName("section_label")
        java_layout.addWidget(jvm_args_label)

        self.jvm_args_input = QLineEdit()
        self.jvm_args_input.setPlaceholderText("-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC")
        self.jvm_args_input.setMinimumHeight(55)
        java_layout.addWidget(self.jvm_args_input)

        # Memory allocation setting
        memory_label = QLabel("MEMORY ALLOCATION (RAM)")
        memory_label.setObjectName("section_label")
        java_layout.addWidget(memory_label)

        memory_layout = QHBoxLayout()
        self.memory_slider = QSlider(Qt.Orientation.Horizontal)
        self.memory_slider.setMinimum(1)
        self.memory_slider.setMaximum(16) # Assuming max 16GB, can be adjusted
        self.memory_slider.setValue(4) # Default 4GB
        self.memory_slider.setTickInterval(1)
        self.memory_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        memory_layout.addWidget(self.memory_slider)

        self.memory_value_label = QLabel("4 GB")
        self.memory_value_label.setObjectName("memory_label")
        self.memory_slider.valueChanged.connect(self.update_memory_label)
        memory_layout.addWidget(self.memory_value_label)
        java_layout.addLayout(memory_layout)
        
        java_layout.addStretch(1)
        self.tabs.addTab(java_tab, "Java & Performance")


        # --- Display & Media Tab ---
        display_tab = QWidget()
        display_layout = QVBoxLayout(display_tab)
        display_layout.setContentsMargins(20, 20, 20, 20)
        display_layout.setSpacing(15)

        # Resolution setting
        resolution_label = QLabel("GAME RESOLUTION")
        resolution_label.setObjectName("section_label")
        display_layout.addWidget(resolution_label)

        resolution_layout = QHBoxLayout()
        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Width")
        self.width_input.setMinimumHeight(55)
        resolution_layout.addWidget(self.width_input)

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Height")
        self.height_input.setMinimumHeight(55)
        resolution_layout.addWidget(self.height_input)
        display_layout.addLayout(resolution_layout)

        # Video Settings
        video_settings_label = QLabel("VIDEO BACKGROUND SETTINGS")
        video_settings_label.setObjectName("section_label")
        display_layout.addWidget(video_settings_label)
        
        self.loop_video_check = QCheckBox("Loop Video/GIF")
        self.loop_video_check.setChecked(True)
        display_layout.addWidget(self.loop_video_check)
        
        self.mute_video_check = QCheckBox("Mute Video Audio")
        self.mute_video_check.setChecked(True)
        display_layout.addWidget(self.mute_video_check)
        
        display_layout.addStretch(1)
        self.tabs.addTab(display_tab, "Display & Media")

        # Save Button (Outside tabs)
        save_button = QPushButton("Save Settings")
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.setMinimumHeight(55)
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button)

        self.load_settings()

    def open_data_directory(self):
        path = MINECRAFT_DIR
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path])
            else: # Assuming Linux
                subprocess.run(["xdg-open", path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open data directory: {e}")

    def browse_file(self, line_edit):
        file, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            line_edit.setText(file)

    def update_memory_label(self, value):
        self.memory_value_label.setText(f"{value} GB")

    def browse_directory(self, line_edit):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            line_edit.setText(directory)

    def load_settings(self):
        self.mods_dir_input.setText(self.config_manager.get("mods_dir", ""))
        self.images_dir_input.setText(self.config_manager.get("images_dir", ""))
        self.java_executable_input.setText(self.config_manager.get("java_executable", ""))
        self.jvm_args_input.setText(self.config_manager.get("jvm_arguments", ""))
        self.memory_slider.setValue(self.config_manager.get("memory_gb", 4))
        self.update_memory_label(self.memory_slider.value())
        self.loop_video_check.setChecked(self.config_manager.get("video_loop", True))
        self.mute_video_check.setChecked(self.config_manager.get("video_mute", True))
        
        resolution = self.config_manager.get("resolution", {})
        self.width_input.setText(resolution.get("width", ""))
        self.height_input.setText(resolution.get("height", ""))

    def save_settings(self):
        self.config_manager.set("mods_dir", self.mods_dir_input.text().strip())
        self.config_manager.set("images_dir", self.images_dir_input.text().strip())
        self.config_manager.set("java_executable", self.java_executable_input.text().strip())
        self.config_manager.set("jvm_arguments", self.jvm_args_input.text().strip())
        self.config_manager.set("memory_gb", self.memory_slider.value())
        self.config_manager.set("video_loop", self.loop_video_check.isChecked())
        self.config_manager.set("video_mute", self.mute_video_check.isChecked())
        self.config_manager.set("resolution", {
            "width": self.width_input.text().strip(),
            "height": self.height_input.text().strip()
        })
        
        self.config_manager.save()
        QMessageBox.information(self, "Settings Saved", "Your settings have been saved. Some changes may require a restart to take effect.")
