from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtProperty, QObject
from PyQt6.QtWidgets import QPushButton, QLineEdit, QGraphicsDropShadowEffect, QWidget
from PyQt6.QtGui import QColor, QPainter, QPen

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None, is_secondary=False, is_destructive=False):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.default_color = QColor("#3b82f6") # Vibrant Blue
        self.hover_color = QColor("#60a5fa")  # Lighter Blue
        self.pressed_color = QColor("#2563eb") # Darker Blue

        if is_secondary:
            self.default_color = QColor(255, 255, 255, 13) # rgba(255,255,255,0.05)
            self.hover_color = QColor(255, 255, 255, 26)  # rgba(255,255,255,0.1)
            self.pressed_color = QColor(255, 255, 255, 5) # rgba(255,255,255,0.02)
        elif is_destructive:
            self.default_color = QColor(239, 68, 68) # Red-500
            self.hover_color = QColor(248, 113, 113) # Red-400
            self.pressed_color = QColor(220, 38, 38) # Red-600

        self._bg_color = self.default_color

        # Add Drop Shadow Glow Effect
        self._shadow_blur = 5.0
        self._shadow_effect = QGraphicsDropShadowEffect(self)
        self._shadow_effect.setBlurRadius(self._shadow_blur)

        # Set shadow color based on button type
        if is_secondary:
             self._shadow_effect.setColor(QColor(0, 0, 0, 0)) # No glow for secondary
        elif is_destructive:
             self._shadow_effect.setColor(QColor(239, 68, 68, 120))
        else:
             self._shadow_effect.setColor(QColor(59, 130, 246, 120)) # Blue glow

        self._shadow_effect.setOffset(0, 0) # Center the glow
        self.setGraphicsEffect(self._shadow_effect)

        self.setStyleSheet(f"""
            QPushButton {{
                color: white;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 15px;
                font-weight: 600;
                border: none;
            }}
        """)

    def _get_bg_color(self):
        return self._bg_color

    def _set_bg_color(self, color):
        self._bg_color = color

        if color.alpha() < 255:
            bg_string = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha() / 255.0:.2f})"
        else:
            bg_string = color.name()

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_string};
                color: white;
                border-radius: 12px;
                padding: 0 24px;
                font-size: 15px;
                font-weight: 700;
                border: 1px solid rgba(255,255,255,0.1);
            }}
        """)

    bg_color = pyqtProperty(QColor, _get_bg_color, _set_bg_color)

    def _get_shadow_blur(self):
        return self._shadow_blur

    def _set_shadow_blur(self, radius):
        self._shadow_blur = radius
        self._shadow_effect.setBlurRadius(radius)

    shadow_blur = pyqtProperty(float, _get_shadow_blur, _set_shadow_blur)

    def enterEvent(self, event):
        self.animate_color(self.hover_color)
        self.animate_glow(25.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_color(self.default_color)
        self.animate_glow(5.0)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.animate_color(self.pressed_color)
        self.animate_glow(10.0)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.underMouse():
            self.animate_color(self.hover_color)
            self.animate_glow(25.0)
        else:
            self.animate_color(self.default_color)
            self.animate_glow(5.0)
        super().mouseReleaseEvent(event)

    def animate_color(self, target_color):
        self.anim = QPropertyAnimation(self, b"bg_color")
        self.anim.setDuration(150)
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(target_color)
        self.anim.start()

    def animate_glow(self, target_radius):
        self.glow_anim = QPropertyAnimation(self, b"shadow_blur")
        self.glow_anim.setDuration(200)
        self.glow_anim.setStartValue(self._shadow_blur)
        self.glow_anim.setEndValue(target_radius)
        self.glow_anim.start()


class ShakeWidget(QObject):
    pass


class AnimatedInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._border_color = QColor("#3a3a3a")
        self.default_border = QColor("#3a3a3a")
        self.focus_border = QColor("#4a9eff")
        self.error_border = QColor("#f44336")

    def shake(self):
        self.setProperty("error", True)
        self.style().unpolish(self)
        self.style().polish(self)
        QTimer.singleShot(500, self.clear_error)

    def clear_error(self):
        self.setProperty("error", False)
        self.style().unpolish(self)
        self.style().polish(self)


class NavIndicatorWidget(QWidget):
    """A sliding pill indicator that overlays nav buttons to show the active item."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("nav_indicator")
        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(220)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def slide_to(self, target_rect: QRect):
        if not self.isVisible():
            self.setGeometry(target_rect)
            self.show()
            return
        self._anim.stop()
        self._anim.setStartValue(self.geometry())
        self._anim.setEndValue(target_rect)
        self._anim.start()


class WindowControlButton(QPushButton):
    """A frameless window control button (min/max/close) with animated background.
    Icons are drawn via QPainter to avoid emoji/font rendering issues on Windows.
    """
    def __init__(self, object_name="", parent=None):
        super().__init__("", parent)
        self.setObjectName(object_name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(46, 40)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        if object_name == "wc_close":
            self._default_color = QColor(0, 0, 0, 0)
            self._hover_color = QColor(232, 17, 35, 230)
            self._pressed_color = QColor(200, 0, 20, 255)
        else:
            self._default_color = QColor(0, 0, 0, 0)
            self._hover_color = QColor(255, 255, 255, 20)
            self._pressed_color = QColor(255, 255, 255, 10)

        self._bg_color = self._default_color
        self._update_style()

    def _get_bg_color(self):
        return self._bg_color

    def _set_bg_color(self, color):
        self._bg_color = color
        self._update_style()

    bg_color = pyqtProperty(QColor, _get_bg_color, _set_bg_color)

    def _update_style(self):
        c = self._bg_color
        bg = f"rgba({c.red()},{c.green()},{c.blue()},{c.alpha()/255.0:.2f})"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                border: none;
                border-radius: 0px;
                padding: 0;
            }}
        """)

    def paintEvent(self, event):
        super().paintEvent(event)  # draws the background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        icon_color = QColor(255, 255, 255, 170)
        pen = QPen(icon_color, 1.4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        cx = self.width() // 2
        cy = self.height() // 2
        s = 5  # half-size of icons

        name = self.objectName()
        if name == "wc_minimize":
            painter.drawLine(cx - s, cy, cx + s, cy)
        elif name == "wc_maximize":
            painter.drawRect(cx - s, cy - s, s * 2, s * 2)
        elif name == "wc_close":
            painter.drawLine(cx - s, cy - s, cx + s, cy + s)
            painter.drawLine(cx + s, cy - s, cx - s, cy + s)

        painter.end()

    def enterEvent(self, event):
        self._animate_to(self._hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_to(self._default_color)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._animate_to(self._pressed_color)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.underMouse():
            self._animate_to(self._hover_color)
        else:
            self._animate_to(self._default_color)
        super().mouseReleaseEvent(event)

    def _animate_to(self, target: QColor):
        self._anim = QPropertyAnimation(self, b"bg_color")
        self._anim.setDuration(120)
        self._anim.setStartValue(self._bg_color)
        self._anim.setEndValue(target)
        self._anim.start()
