import sys
import cv2
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                qt_img = QImage(cv_img.data, cv_img.shape[1], cv_img.shape[0], QImage.Format_RGB888)
                self.change_pixmap_signal.emit(qt_img)

    def stop(self):
        self._run_flag = False
        self.wait()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Camera'
        self.left = 100
        self.top = 100
        self.width = 800  # Increased width for both labels
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Image label for webcam feed
        self.image_label = QLabel(self)
        self.image_label.resize(640, 480)

        # Example label for a static image (optional)
        example_image_path = "IdCard"
        pixmap = QPixmap(example_image_path)
        self.example_label = QLabel(self)
        self.example_label.resize(430, 270)
        self.example_label.setPixmap(pixmap.scaled(430, 270))

        # Layouts
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.example_label)

        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

        # Buttons
        btn_layout = QHBoxLayout()

        capture_btn = QPushButton("Capture", self)
        capture_btn.clicked.connect(self.capture_image)
        btn_layout.addWidget(capture_btn)

        stop_btn = QPushButton("Stop", self)
        stop_btn.clicked.connect(self.stop_camera)
        btn_layout.addWidget(stop_btn)

        vbox.addLayout(btn_layout)

        # Camera thread
        self.thread = CameraThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def capture_image(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            pixmap.save("capture.png")
        else:
            print("No image to capture.")

    def update_image(self, qt_img):
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))

    def stop_camera(self):
        self.thread.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
