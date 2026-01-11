from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtProperty, QObject
from PyQt6.QtWidgets import QPushButton, QLineEdit, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None, is_secondary=False, is_destructive=False):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.default_color = QColor("#4a9eff")
        self.hover_color = QColor("#5badff")
        self.pressed_color = QColor("#3a8eef")
        
        if is_secondary:
            self.default_color = QColor("#3c3c3c")
            self.hover_color = QColor("#4a4a4a")
            self.pressed_color = QColor("#303030")
        elif is_destructive:
            self.default_color = QColor(200, 50, 50)
            self.hover_color = QColor(220, 70, 70)
            self.pressed_color = QColor(180, 40, 40)
            
        self._bg_color = self.default_color
        
        # Stylesheet base - we handle background color via animation, 
        # so remove background-color from stylesheet if we want pure py animation,
        # OR we just animate a property that updates stylesheet.
        # But QPropertyAnimation on "styleSheet" is inefficient.
        # Better: use QObject property and paint event override OR simple qss transition?
        # PyQt doesn't support CSS transitions.
        # We will use a custom property for background color.
        
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
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                color: white;
                border-radius: 8px;
                padding: 0 20px;
                font-size: 15px;
                font-weight: 600;
                border: none;
            }}
        """)

    bg_color = pyqtProperty(QColor, _get_bg_color, _set_bg_color)

    def enterEvent(self, event):
        self.animate_color(self.hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_color(self.default_color)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.animate_color(self.pressed_color)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.underMouse():
            self.animate_color(self.hover_color)
        else:
            self.animate_color(self.default_color)
        super().mouseReleaseEvent(event)

    def animate_color(self, target_color):
        self.anim = QPropertyAnimation(self, b"bg_color")
        self.anim.setDuration(150)
        self.anim.setStartValue(self._bg_color)
        self.anim.setEndValue(target_color)
        self.anim.start()


class ShakeWidget(QObject): # Mixin or helper?
    pass # implementing directly in widget for now for simplicity

class AnimatedInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._border_color = QColor("#3a3a3a")
        self.default_border = QColor("#3a3a3a")
        self.focus_border = QColor("#4a9eff")
        self.error_border = QColor("#f44336")
        
        # Initial style updates happen via qss usually, but we want to animate border.
        # Animatng border in QSS is hard via property.
        # We'll just stick to QSS with simple state changes for now, 
        # OR animate a "borderColor" property.
        
    def shake(self):
        # Simple shake animation
        key_pos = self.pos()
        x = key_pos.x()
        y = key_pos.y()
        
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(50)
        self.anim.setLoopCount(5)
        
        # Shake sequence: left, right, left, right...
        # Note: 'pos' animation on a widget in a layout might be fought by layout.
        # Better to simple set style to error and flash it.
        self.setProperty("error", True)
        self.style().unpolish(self)
        self.style().polish(self)
        
        QTimer.singleShot(500, self.clear_error)

    def clear_error(self):
        self.setProperty("error", False)
        self.style().unpolish(self)
        self.style().polish(self)
