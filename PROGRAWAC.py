from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QSlider, QLabel
from PyQt5.QtCore import QUrl, Qt
import sys

class MusicPlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.setVolume(50)


        self.setWindowTitle("Music Player")
        self.setGeometry(300, 300, 500, 200)
        self.setStyleSheet("background-color: #f0f0f0; font-family: Arial;")


        self.openButton = QtWidgets.QPushButton("🎶 Open")
        self.openButton.setStyleSheet("font-size: 16px; padding: 10px;")
        self.openButton.clicked.connect(self.open_file)

        self.playButton = QtWidgets.QPushButton("▶️ Play")
        self.playButton.setStyleSheet("font-size: 16px; padding: 10px;")
        self.playButton.clicked.connect(self.play_music)

        self.pauseButton = QtWidgets.QPushButton("⏸️ Pause")
        self.pauseButton.setStyleSheet("font-size: 16px; padding: 10px;")
        self.pauseButton.clicked.connect(self.pause_music)

        self.stopButton = QtWidgets.QPushButton("⏹️ Stop")
        self.stopButton.setStyleSheet("font-size: 16px; padding: 10px;")
        self.stopButton.clicked.connect(self.stop_music)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.set_volume)
        self.volumeSlider.setStyleSheet("height: 10px;")


        self.volumeLabel = QLabel("Volume:")
        self.volumeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        self.trackSlider = QSlider(Qt.Horizontal)
        self.trackSlider.setRange(0, 100)
        self.trackSlider.sliderMoved.connect(self.set_position)
        self.trackSlider.setStyleSheet("height: 10px;")
        

        self.mediaPlayer.positionChanged.connect(self.update_position)
        self.mediaPlayer.durationChanged.connect(self.update_duration)

        layout = QtWidgets.QVBoxLayout()
        controlsLayout = QtWidgets.QHBoxLayout()
        volumeLayout = QtWidgets.QHBoxLayout()

        layout.addWidget(self.openButton)
        layout.addWidget(self.trackSlider)

        controlsLayout.addWidget(self.playButton)
        controlsLayout.addWidget(self.pauseButton)
        controlsLayout.addWidget(self.stopButton)
        layout.addLayout(controlsLayout)

        volumeLayout.addWidget(self.volumeLabel)
        volumeLayout.addWidget(self.volumeSlider)
        layout.addLayout(volumeLayout)

        self.setLayout(layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Music File", "", "Audio Files (*.mp3 *.wav)")
        if file_name:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.play_music()

    def play_music(self):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.NoMedia:
            self.open_file()
        self.mediaPlayer.play()

    def pause_music(self):
        self.mediaPlayer.pause()

    def stop_music(self):
        self.mediaPlayer.stop()

    def set_volume(self, value):
        self.mediaPlayer.setVolume(value)

    def update_position(self, position):
        self.trackSlider.setValue(position)

    def update_duration(self, duration):
        self.trackSlider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
