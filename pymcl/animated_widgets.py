from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtProperty, QObject
from PyQt6.QtWidgets import QPushButton, QLineEdit, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

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
        
        # We handle secondary buttons differently to allow transparent backgrounds
        if color.alpha() < 255:
            # We use rgba string formatting for transparency
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
        self.animate_glow(25.0) # Intensify glow
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_color(self.default_color)
        self.animate_glow(5.0) # Reduce glow
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
