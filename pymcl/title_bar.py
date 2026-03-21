from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy

from .animated_widgets import WindowControlButton
from .constants import APP_NAME


class TitleBar(QWidget):
    """Custom frameless window title bar with drag-to-move and window controls."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("title_bar")
        self.setFixedHeight(40)
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setSpacing(0)

        app_name = QLabel(APP_NAME)
        app_name.setObjectName("titlebar_app_name")
        layout.addWidget(app_name)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(spacer)

        self.btn_minimize = WindowControlButton("wc_minimize", self)
        self.btn_maximize = WindowControlButton("wc_maximize", self)
        self.btn_close = WindowControlButton("wc_close", self)

        self.btn_minimize.clicked.connect(lambda: self.window().showMinimized())
        self.btn_maximize.clicked.connect(self._toggle_maximize)
        self.btn_close.clicked.connect(lambda: self.window().close())

        layout.addWidget(self.btn_minimize)
        layout.addWidget(self.btn_maximize)
        layout.addWidget(self.btn_close)

    def _toggle_maximize(self):
        win = self.window()
        if win.isMaximized():
            win.showNormal()
        else:
            win.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            # Un-maximize if dragging from maximized state
            if self.window().isMaximized():
                self.window().showNormal()
                # Recalculate drag position relative to the restored window
                self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._toggle_maximize()
        super().mouseDoubleClickEvent(event)
