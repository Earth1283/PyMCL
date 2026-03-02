STYLESHEET = """
QWidget {
    background-color: transparent;
    color: #f3f4f6;
    font-family: system-ui, -apple-system, Inter, "Segoe UI", sans-serif;
    font-size: 14px;
}
QMainWindow {
    background-color: #0f1115;
}
QFrame#central_widget_frame {
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    background-color: rgba(15, 17, 21, 0.65);
    padding: 15px;
}
QWidget#card_container {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
}
QLabel {
    color: #e0e0e0;
    font-size: 13px;
    background: transparent;
}
QLabel#title_label {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    padding: 0px;
    background: transparent;
    letter-spacing: -0.5px;
}
QLabel#subtitle_label {
    font-size: 15px;
    color: #888;
    background: transparent;
    margin-top: 5px;
}
QLabel#section_label {
    font-size: 12px;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    background: transparent;
}
QLineEdit {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 0 18px;
    font-size: 15px;
    color: #ffffff;
    min-height: 55px;
}
QLineEdit:focus {
    border: 1px solid #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
}
QLineEdit:hover {
    border: 1px solid rgba(255, 255, 255, 0.2);
    background-color: rgba(255, 255, 255, 0.06);
}
QComboBox {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 0 18px;
    font-size: 15px;
    color: #ffffff;
    min-height: 55px;
}
QComboBox:focus {
    border: 1px solid #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
}
QComboBox:hover {
    border: 1px solid rgba(255, 255, 255, 0.2);
    background-color: rgba(255, 255, 255, 0.06);
}
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #888;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #1f2228;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
    padding: 6px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    padding: 10px 16px;
    border-radius: 8px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: rgba(255, 255, 255, 0.05);
}
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 #2563eb);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 0 24px;
    font-size: 15px;
    font-weight: 700;
    min-height: 55px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #60a5fa, stop:1 #3b82f6);
}
QPushButton:pressed {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);
}
QPushButton:disabled {
    background-color: rgba(255, 255, 255, 0.05);
    color: #6b7280;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

QPushButton#secondary_button {
    background-color: rgba(255, 255, 255, 0.05);
    color: #e5e7eb;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
QPushButton#secondary_button:hover {
    background-color: rgba(255, 255, 255, 0.1);
}
QPushButton#secondary_button:pressed {
    background-color: rgba(255, 255, 255, 0.02);
}
QPushButton#danger_button {
    background-color: rgba(255, 80, 80, 0.2);
    color: #ff8080;
    border: 1px solid rgba(255, 80, 80, 0.5);
}
QPushButton#danger_button:hover {
    background-color: rgba(255, 80, 80, 0.3);
    border-color: rgba(255, 80, 80, 0.7);
}
QPushButton#danger_button:pressed {
    background-color: rgba(255, 80, 80, 0.4);
}
QPushButton[class="destructive"] {
    background-color: rgba(255, 80, 80, 0.8);
    color: #ffffff;
    border: 1px solid rgba(255, 80, 80, 1.0);
}
QPushButton[class="destructive"]:hover {
    background-color: rgba(255, 60, 60, 1.0);
    border-color: rgba(255, 60, 60, 1.0);
}
QProgressBar {
    border: none;
    border-radius: 12px;
    text-align: center;
    background-color: rgba(255, 255, 255, 0.05);
    color: #ffffff;
    font-weight: 700;
    font-size: 13px;
    min-height: 40px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #8b5cf6, stop:1 #3b82f6);
    border-radius: 12px;
}
QLabel#status_label {
    color: #a1a1aa;
    font-size: 13px;
    background: transparent;
    padding: 8px;
}

QCheckBox {
    spacing: 10px;
    font-size: 15px;
    font-weight: 600;
    color: #f0f0f0;
    background: transparent;
}
QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #505050;
    border-radius: 4px;
    background-color: #1e1e1e;
}
QCheckBox::indicator:hover {
    border-color: #606060;
}
QCheckBox::indicator:checked {
    background-color: #4a9eff;
    border-color: #4a9eff;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white' width='18px' height='18px'%3E%3Cpath d='M0 0h24v24H0z' fill='none'/%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
}

QListWidget {
    background-color: #1e1e1e;
    border: 2px solid #3a3a3a;
    border-radius: 8px;
    padding: 5px;
    font-size: 14px;
}
QListWidget::item {
    padding: 8px 12px;
    border-radius: 4px;
    color: #f0f0f0;
}
QListWidget::item:hover {
    background-color: #2a2a2a;
}
QListWidget::item:selected {
    background-color: #4a9eff;
    color: #ffffff;
}

QWidget#main_central_widget {
    background: transparent;
}

QWidget#left_title_container {
    background-color: rgba(15, 17, 21, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 15px;
}

QFrame#title_frame {
    background-color: transparent;
    border-radius: 16px;
    border: none;
}

QDialog {
    background-color: #252525;
}

QPushButton#nav_button, QPushButton#nav_button_active {
    background-color: transparent;
    border: 1px solid transparent;
    color: #9ca3af;
    font-size: 15px;
    font-weight: 600;
    text-align: left;
    padding: 12px 20px;
    border-radius: 12px;
    min-height: 48px;
}

QPushButton#nav_button:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #ffffff;
}

QPushButton#nav_button_active {
    background-color: rgba(59, 130, 246, 0.1);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.2);
}
QSlider::groove:horizontal {
    border: 1px solid #3a3a3a;
    height: 4px;
    background: #1e1e1e;
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #4a9eff;
    border: 1px solid #4a9eff;
    width: 18px;
    height: 18px;
    margin: -8px 0;
    border-radius: 9px;
}

QSlider::add-page:horizontal {
    background: #1e1e1e;
}

QSlider::sub-page:horizontal {
    background: #4a9eff;
}

QScrollArea#content_scroll_area {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    border: none;
    background: rgba(255, 255, 255, 0.02);
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.2);
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.3);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: rgba(255, 255, 255, 0.02);
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.2);
    min-width: 20px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: rgba(255, 255, 255, 0.3);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QMenuBar {
    background-color: #1a1a1a;
    color: #f0f0f0;
    spacing: 10px;
}
QMenuBar::item {
    padding: 5px 10px;
    background: transparent;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #3c3c3c;
}
QMenu {
    background-color: #2d2d2d;
    color: #f0f0f0;
    border: 1px solid #3c3c3c;
    padding: 5px;
}
QMenu::item {
    padding: 8px 25px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #4a9eff;
}
QMenu::separator {
    height: 1px;
    background: #3c3c3c;
    margin: 5px 0;
}

/* Mod Browser */
QWidget#floating_search_container {
    background-color: rgba(37, 37, 37, 0.95);
    border-bottom: 1px solid #3a3a3a;
}
QWidget#mod_card {
    background-color: #2a2a2a;
    border-radius: 8px;
    border: 1px solid #3a3a3a;
    padding: 15px;
}
QWidget#mod_card:hover {
    border-color: #4a9eff;
}
QLabel#mod_card_title {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
}
QLabel#mod_card_downloads {
    font-size: 12px;
    color: #888;
}
QPushButton#download_badge {
    background-color: #4a9eff;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 5px 15px;
    font-size: 12px;
    font-weight: 600;
    min-height: 24px;
}
QPushButton#download_badge:hover {
    background-color: #5badff;
}

/* Tab Widget */
QTabWidget::pane {
    border: none;
    background-color: transparent;
    top: 10px;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background: rgba(255, 255, 255, 0.03);
    color: #9ca3af;
    padding: 10px 24px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin: 0 4px;
    font-weight: 600;
}

QTabBar::tab:selected {
    background: rgba(59, 130, 246, 0.15);
    color: #ffffff;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

QTabBar::tab:hover:!selected {
    background: rgba(255, 255, 255, 0.08);
    color: #e5e7eb;
}

/* Toast Notifications */
QWidget[class^="Toast_"] {
    background-color: #252525;
    border: 1px solid #333;
    border-radius: 8px;
    min-height: 50px;
}

QWidget#Toast_INFO {
    border-left: 4px solid #4a9eff;
}

QWidget#Toast_SUCCESS {
    border-left: 4px solid #4caf50;
    background-color: #1e261e; /* Subtle green tint */
}

QWidget#Toast_WARNING {
    border-left: 4px solid #ff9800;
    background-color: #26221e; /* Subtle orange tint */
}

QWidget#Toast_ERROR {
    border-left: 4px solid #f44336;
    background-color: #261e1e; /* Subtle red tint */
}

QLabel#toast_title {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#toast_message {
    font-size: 13px;
    color: #ccc;
}

QPushButton#toast_close {
    background: transparent;
    color: #666;
    border: none;
    font-weight: bold;
    font-size: 16px;
}
QPushButton#toast_close:hover {
    color: #fff;
}
"""
