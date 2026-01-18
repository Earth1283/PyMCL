from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QLabel,
    QMessageBox
)
from .server_status_widget import ServerCard
from .config_manager import ConfigManager

class ServersPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.server_list = [] # List of IPs

        self.init_ui()
        self.load_servers()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # -- Add Server Section --
        add_container = QWidget()
        add_layout = QHBoxLayout(add_container)
        add_layout.setContentsMargins(20, 20, 20, 0)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter server address (e.g. hypixel.net)")
        self.ip_input.setMinimumHeight(45)
        self.ip_input.returnPressed.connect(self.add_server)
        add_layout.addWidget(self.ip_input)

        self.add_button = QPushButton("Add Server")
        self.add_button.setObjectName("secondary_button")
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setMinimumHeight(45)
        self.add_button.clicked.connect(self.add_server)
        add_layout.addWidget(self.add_button)

        layout.addWidget(add_container)

        # -- Server List Area --
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("content_scroll_area")

        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(20, 20, 20, 20)
        self.list_layout.setSpacing(15)
        self.list_layout.addStretch(1) # Push items to top

        scroll_area.setWidget(self.list_container)
        layout.addWidget(scroll_area)

    def load_servers(self):
        # Clear existing
        self.clear_list_ui()

        # Load from config
        self.server_list = self.config_manager.get("saved_servers", [])

        if not self.server_list:
            # Default empty state or welcome server
            self.add_server_card("hypixel.net") # Example default
            if "hypixel.net" not in self.server_list:
                self.server_list.append("hypixel.net")
                self.save_servers()
        else:
            for ip in self.server_list:
                self.add_server_card(ip)

    def save_servers(self):
        self.config_manager.set("saved_servers", self.server_list)
        self.config_manager.save()

    def clear_list_ui(self):
        # Remove all widgets from layout except the stretch
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    @pyqtSlot()
    def add_server(self):
        ip = self.ip_input.text().strip()
        if not ip:
            return

        if ip in self.server_list:
            QMessageBox.warning(self, "Duplicate", "This server is already in your list.")
            return

        self.server_list.append(ip)
        self.save_servers()
        self.add_server_card(ip)
        self.ip_input.clear()

    def add_server_card(self, ip):
        card = ServerCard(ip)
        card.remove_requested.connect(self.remove_server)
        # Insert before stretch (index = count - 1)
        self.list_layout.insertWidget(self.list_layout.count() - 1, card)

    @pyqtSlot(str)
    def remove_server(self, ip):
        if ip in self.server_list:
            self.server_list.remove(ip)
            self.save_servers()

            # Find and remove widget
            for i in range(self.list_layout.count()):
                item = self.list_layout.itemAt(i)
                widget = item.widget()
                if isinstance(widget, ServerCard) and widget.ip == ip:
                    widget.deleteLater()
                    break
