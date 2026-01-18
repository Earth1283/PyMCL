from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QColor, QAction, QFontDatabase
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QApplication,
    QCheckBox,
    QLabel,
    QFrame
)

class ConsoleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Game Console")
        self.resize(900, 650)
        self.auto_scroll = True

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QFrame()
        toolbar.setStyleSheet("background-color: #252526; border-bottom: 1px solid #333;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 8, 10, 8)

        title = QLabel("Output Log")
        title.setStyleSheet("font-weight: bold; color: #ddd; font-size: 13px;")
        toolbar_layout.addWidget(title)

        toolbar_layout.addStretch(1)

        self.auto_scroll_check = QCheckBox("Auto-scroll")
        self.auto_scroll_check.setChecked(True)
        self.auto_scroll_check.setStyleSheet("color: #ccc;")
        self.auto_scroll_check.toggled.connect(self.set_auto_scroll)
        toolbar_layout.addWidget(self.auto_scroll_check)

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_logs)
        toolbar_layout.addWidget(self.copy_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_logs)
        toolbar_layout.addWidget(self.clear_btn)

        layout.addWidget(toolbar)

        # Console Output
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setObjectName("console_output")
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap) # Logs are better without wrap usually

        # Font selection
        preferred_fonts = ["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas", "Menlo", "Courier New"]
        font_family = "Monospace"
        for font in preferred_fonts:
            if font in QFontDatabase.families():
                font_family = font
                break

        font = QFont(font_family)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(10)
        self.text_edit.setFont(font)

        layout.addWidget(self.text_edit)

        # Apply Dark Theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: none;
                padding: 5px;
                selection-background-color: #264f78;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
            QScrollBar:vertical {
                border: none;
                background: #1e1e1e;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                min-height: 20px;
                border-radius: 0px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4f4f4f;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border: 1px solid #555;
                border-radius: 2px;
                background: #1e1e1e;
            }
            QCheckBox::indicator:checked {
                background: #007acc;
                border-color: #007acc;
            }
        """)

    def set_auto_scroll(self, checked):
        self.auto_scroll = checked

    @pyqtSlot(str)
    def append_log(self, text):
        # Basic color highlighting
        color = "#cccccc" # default gray
        if "[ERROR]" in text or "Exception" in text or "at " in text or "FATAL" in text:
            color = "#ff6b6b" # soft red
        elif "[WARN]" in text:
            color = "#f1c40f" # yellow
        elif "[INFO]" in text:
            color = "#6ab04c" # green
        elif "DEBUG" in text:
            color = "#569cd6" # blue

        formatted_text = f'<span style="color:{color};">{text}</span>'
        self.text_edit.append(formatted_text)

        if self.auto_scroll:
            scrollbar = self.text_edit.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def copy_logs(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())

    def clear_logs(self):
        self.text_edit.clear()
