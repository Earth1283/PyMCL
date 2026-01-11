from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, QObject
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QPushButton
from PyQt6.QtGui import QColor, QIcon

class ToastNotification(QWidget):
    def __init__(self, parent, title, message, type_name="INFO", duration=3000):
        super().__init__(parent)
        self.duration = duration
        
        # Setup UI
        self.setObjectName(f"Toast_{type_name}")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)
        
        # Text container
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        if title:
            self.title_label = QLabel(title)
            self.title_label.setObjectName("toast_title")
            text_layout.addWidget(self.title_label)
        
        self.message_label = QLabel(message)
        self.message_label.setObjectName("toast_message")
        self.message_label.setWordWrap(True)
        text_layout.addWidget(self.message_label)
        
        layout.addLayout(text_layout)
        
        # Close button (tiny 'x')
        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("toast_close")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.clicked.connect(self.close_toast)
        layout.addWidget(self.close_btn, 0, Qt.AlignmentFlag.AlignTop)
        
        # Opacity Effect for animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self.opacity_effect)
        
        # Timer for auto-close
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close_toast)
        
        self.hide() # Start hidden
        
    def show_toast(self):
        self.show()
        self.raise_()
        
        # Animate In
        self.anim_group = QParallelAnimationGroup()
        
        # Opacity
        anim_opacity = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim_opacity.setStartValue(0.0)
        anim_opacity.setEndValue(1.0)
        anim_opacity.setDuration(400)
        anim_opacity.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_group.addAnimation(anim_opacity)
        
        self.anim_group.start()
        
        self.timer.start(self.duration)

    def close_toast(self):
        self.timer.stop()
        
        # Notify manager to remove from active list immediately to update positions
        if hasattr(self, 'manager'):
            self.manager.remove_toast(self)
        
        self.anim_group = QParallelAnimationGroup()
        
        # Opacity
        anim_opacity = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim_opacity.setStartValue(1.0)
        anim_opacity.setEndValue(0.0)
        anim_opacity.setDuration(300)
        anim_opacity.setEasingCurve(QEasingCurve.Type.InCubic)
        
        self.anim_group.addAnimation(anim_opacity)
        self.anim_group.finished.connect(self.close) # Close widget when done
        self.anim_group.finished.connect(self.deleteLater)
        
        self.anim_group.start()


class ToastManager(QObject):
    def __init__(self, parent_widget):
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.active_toasts = []
        self.toast_width = 320
        self.spacing = 10
        self.margin_right = 20
        self.margin_top = 20
        
    def show_toast(self, message, title="", type_name="INFO", duration=3000):
        # Create toast with parent as the main window
        toast = ToastNotification(self.parent_widget, title, message, type_name, duration)
        toast.manager = self
        toast.setFixedWidth(self.toast_width)
        
        # Initial postion (will be updated)
        # We start it at the target position but invisible
        self.active_toasts.append(toast)
        self.reposition_toasts()
        toast.show_toast()
        
    def remove_toast(self, toast):
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
            self.reposition_toasts()

    def reposition_toasts(self):
        # Calculate positions
        current_y = self.margin_top
        
        for toast in self.active_toasts:
            # Target geometry
            target_x = self.parent_widget.width() - self.toast_width - self.margin_right
            target_y = current_y
            
            # If toast is just created (not visible), set its pos directly
            if not toast.isVisible():
                toast.move(target_x, target_y)
            else:
                # Animate to new position
                if not hasattr(toast, 'pos_anim'):
                     toast.pos_anim = QPropertyAnimation(toast, b"pos")
                     toast.pos_anim.setDuration(300)
                     toast.pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
                
                toast.pos_anim.stop()
                toast.pos_anim.setEndValue(QPoint(target_x, target_y))
                toast.pos_anim.start()

            # Ensure layout is up to date to get correct height
            toast.adjustSize()
            height = toast.height()
            
            # Additional check to ensure minimum visual height
            if height < 60: 
                height = 60

            current_y += height + self.spacing
