from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QMovie, QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QStackedLayout,
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.layout = QStackedLayout(self)
        self.layout.setStackingMode(QStackedLayout.StackingMode.StackOne)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Image/GIF Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)

        # Video
        self.video_widget = QVideoWidget()
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.player.errorOccurred.connect(self._on_media_error)
        self.layout.addWidget(self.video_widget)

        self.movie = None

    def _on_media_error(self, error, error_string):
        print(f"Media Player Error: {error} - {error_string}")

    def set_image(self, path):
        self.player.stop()
        if self.movie:
            self.movie.stop()
            self.movie = None

        pixmap = QPixmap(path)
        self.image_label.setPixmap(pixmap)
        self.layout.setCurrentWidget(self.image_label)

    def set_gif(self, path):
        self.player.stop()
        if self.movie:
            self.movie.stop()

        self.movie = QMovie(path)
        self.image_label.setMovie(self.movie)
        self.movie.start()
        self.layout.setCurrentWidget(self.image_label)

    def set_video(self, path, loop=True, mute=True):
        if self.movie:
            self.movie.stop()
            self.movie = None

        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.setLoops(QMediaPlayer.Loops.Infinite if loop else 1)
        self.audio_output.setMuted(mute)

        self.layout.setCurrentWidget(self.video_widget)
        self.player.play()
