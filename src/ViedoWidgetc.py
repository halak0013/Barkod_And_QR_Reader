import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import  QLabel


class VideoWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)

    def show_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = channel * width
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.setPixmap(pixmap)


class VideoThread(QThread):
    frame_available = pyqtSignal(np.ndarray)

    def __init__(self,video_capture):
        super().__init__()
        self.video_capture = video_capture

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                self.frame_available.emit(frame)