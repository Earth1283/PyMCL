import os
import shutil

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QListWidget

from .constants import MODS_DIR


class ModListWidget(QListWidget):
    mods_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.DropOnly)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile() and url.toLocalFile().endswith(".jar"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        copied_count = 0
        for url in event.mimeData().urls():
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if file_path.endswith(".jar"):
                    try:
                        filename = os.path.basename(file_path)
                        dest_path = os.path.join(MODS_DIR, filename)
                        shutil.copy(file_path, dest_path)
                        print(f"Copied mod {filename} to {MODS_DIR}")
                        copied_count += 1
                    except Exception as e:
                        print(f"Error copying mod {file_path}: {e}")

        if copied_count > 0:
            self.mods_changed.emit()
