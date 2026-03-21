STYLESHEET = """
QWidget {
    background-color: transparent;
    color: #f3f4f6;
    font-family: Inter, "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
}
QMainWindow {
    background-color: #0d1015;
}

/* ── Outer rounded app card ── */
QFrame#app_outer_frame {
    background-color: rgba(13, 16, 21, 0.93);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
}

/* ── Custom title bar ── */
QWidget#title_bar {
    background: transparent;
    border-top-left-radius: 14px;
    border-top-right-radius: 14px;
    min-height: 40px;
    max-height: 40px;
}
QLabel#titlebar_app_name {
    font-size: 12px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.35);
    letter-spacing: 0.8px;
    background: transparent;
}

/* ── Content frame (right panel) ── */
QFrame#central_widget_frame {
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    background-color: rgba(15, 17, 21, 0.60);
    padding: 10px;
}

/* ── Cards ── */
QWidget#card_container {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 10px;
}

/* ── Labels ── */
QLabel {
    color: #e0e0e0;
    font-size: 13px;
    background: transparent;
}
QLabel#title_label {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    padding: 0px;
    background: transparent;
    letter-spacing: 0px;
}
QLabel#subtitle_label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.35);
    background: transparent;
    margin-top: 4px;
}
QLabel#section_label {
    font-size: 10px;
    font-weight: 700;
    color: rgba(156, 163, 175, 0.7);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    background: transparent;
}
QLabel#status_label {
    color: #71717a;
    font-size: 12px;
    background: transparent;
    padding: 6px;
}

/* ── Inputs ── */
QLineEdit {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 8px;
    padding: 0 14px;
    font-size: 14px;
    color: #ffffff;
    min-height: 42px;
}
QLineEdit:focus {
    border: 1px solid #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
}
QLineEdit:hover {
    border: 1px solid rgba(255, 255, 255, 0.18);
    background-color: rgba(255, 255, 255, 0.05);
}

/* ── ComboBox ── */
QComboBox {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 8px;
    padding: 0 14px;
    font-size: 14px;
    color: #ffffff;
    min-height: 42px;
}
QComboBox:focus {
    border: 1px solid #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
}
QComboBox:hover {
    border: 1px solid rgba(255, 255, 255, 0.18);
    background-color: rgba(255, 255, 255, 0.05);
}
QComboBox::drop-down {
    border: none;
    width: 25px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #888;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #1a1d23;
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 8px;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
    padding: 4px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 6px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

/* ── Buttons ── */
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 #2563eb);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 0 18px;
    font-size: 14px;
    font-weight: 700;
    min-height: 42px;
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

/* ── Progress Bar ── */
QProgressBar {
    border: none;
    border-radius: 8px;
    text-align: center;
    background-color: rgba(255, 255, 255, 0.05);
    color: #ffffff;
    font-weight: 700;
    font-size: 12px;
    min-height: 32px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #8b5cf6, stop:1 #3b82f6);
    border-radius: 8px;
}

/* ── Checkbox ── */
QCheckBox {
    spacing: 8px;
    font-size: 14px;
    font-weight: 600;
    color: #f0f0f0;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
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

/* ── List Widget ── */
QListWidget {
    background-color: #1a1d23;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 4px;
    font-size: 13px;
}
QListWidget::item {
    padding: 6px 10px;
    border-radius: 6px;
    color: #f0f0f0;
}
QListWidget::item:hover {
    background-color: rgba(255, 255, 255, 0.05);
}
QListWidget::item:selected {
    background-color: #4a9eff;
    color: #ffffff;
}

/* ── Main central widget (transparent overlay) ── */
QWidget#main_central_widget {
    background: transparent;
}

/* ── Left sidebar ── */
QWidget#left_title_container {
    background-color: rgba(10, 12, 18, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 0px;
}
QFrame#title_frame {
    background-color: transparent;
    border-radius: 10px;
    border: none;
}

/* ── Sidebar bottom area ── */
QWidget#sidebar_bottom {
    background: transparent;
}
QFrame#sidebar_separator {
    background-color: rgba(255, 255, 255, 0.07);
    border: none;
    max-height: 1px;
    margin: 0 8px;
}
QLabel#sidebar_version_label {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.22);
    background: transparent;
    padding: 2px 6px;
}

/* ── Nav buttons ── */
QPushButton#nav_button {
    background-color: transparent;
    border: 1px solid transparent;
    color: rgba(229, 231, 235, 0.55);
    font-size: 14px;
    font-weight: 600;
    text-align: left;
    padding: 10px 15px 10px 18px;
    border-radius: 10px;
    min-height: 40px;
}
QPushButton#nav_button:hover {
    color: rgba(255, 255, 255, 0.85);
}
QPushButton#nav_button[active="true"] {
    color: #60a5fa;
    font-weight: 700;
}

/* ── Sliding nav indicator ── */
QWidget#nav_indicator {
    background-color: rgba(59, 130, 246, 0.11);
    border: 1px solid rgba(59, 130, 246, 0.22);
    border-radius: 10px;
}

/* ── Dialogs ── */
QDialog {
    background-color: #1a1d23;
}

/* ── Slider ── */
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
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}
QSlider::add-page:horizontal {
    background: #1e1e1e;
}
QSlider::sub-page:horizontal {
    background: #4a9eff;
}

/* ── Scroll areas ── */
QScrollArea#content_scroll_area {
    background: transparent;
    border: none;
}
QScrollBar:vertical {
    border: none;
    background: rgba(255, 255, 255, 0.02);
    width: 6px;
    margin: 0px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.18);
    min-height: 15px;
    border-radius: 3px;
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
    height: 6px;
    margin: 0px;
    border-radius: 3px;
}
QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.18);
    min-width: 15px;
    border-radius: 3px;
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

/* ── Menu bar (hidden, but styled in case visible) ── */
QMenuBar {
    background-color: #12151a;
    color: #f0f0f0;
    spacing: 8px;
}
QMenuBar::item {
    padding: 4px 8px;
    background: transparent;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #2a2d35;
}
QMenu {
    background-color: #1a1d23;
    color: #f0f0f0;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 4px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #4a9eff;
}
QMenu::separator {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 4px 0;
}

/* ── Mod Browser ── */
QWidget#floating_search_container {
    background-color: rgba(22, 25, 32, 0.95);
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
QWidget#mod_card {
    background-color: rgba(255,255,255,0.03);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.07);
    padding: 10px;
}
QWidget#mod_card:hover {
    border-color: rgba(59, 130, 246, 0.4);
}
QLabel#mod_card_title {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
}
QLabel#mod_card_downloads {
    font-size: 11px;
    color: rgba(255,255,255,0.4);
}
QPushButton#download_badge {
    background-color: #4a9eff;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
    min-height: 20px;
}
QPushButton#download_badge:hover {
    background-color: #5badff;
}

/* ── Tab Widget ── */
QTabWidget::pane {
    border: none;
    background-color: transparent;
    top: 6px;
}
QTabWidget::tab-bar {
    alignment: center;
}
QTabBar::tab {
    background: rgba(255, 255, 255, 0.03);
    color: #9ca3af;
    padding: 6px 18px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin: 0 4px;
    font-weight: 600;
}
QTabBar::tab:selected {
    background: rgba(59, 130, 246, 0.14);
    color: #ffffff;
    border: 1px solid rgba(59, 130, 246, 0.28);
}
QTabBar::tab:hover:!selected {
    background: rgba(255, 255, 255, 0.07);
    color: #e5e7eb;
}

/* ── Toast Notifications ── */
QWidget[class^="Toast_"] {
    background-color: #1a1d23;
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 8px;
    min-height: 40px;
}
QWidget#Toast_INFO {
    border-left: 3px solid #4a9eff;
}
QWidget#Toast_SUCCESS {
    border-left: 3px solid #4caf50;
    background-color: #161f16;
}
QWidget#Toast_WARNING {
    border-left: 3px solid #ff9800;
    background-color: #1f1a13;
}
QWidget#Toast_ERROR {
    border-left: 3px solid #f44336;
    background-color: #1f1313;
}
QLabel#toast_title {
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
}
QLabel#toast_message {
    font-size: 12px;
    color: rgba(255,255,255,0.6);
}
QPushButton#toast_close {
    background: transparent;
    color: rgba(255,255,255,0.35);
    border: none;
    font-weight: bold;
    font-size: 14px;
}
QPushButton#toast_close:hover {
    color: #fff;
}
"""
