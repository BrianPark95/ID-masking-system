import sys
import cv2
import easyocr
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRect
import numpy as np

class ImageMosaicApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('IdCard OCR')
        self.setGeometry(100, 100, 720, 360)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(430, 270)

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignLeft)
        self.result_label.setWordWrap(True)

        self.mosaic_checkbox1 = QCheckBox('Name', self)
        self.mosaic_checkbox1.stateChanged.connect(self.toggleMosaic)

        self.mosaic_checkbox2 = QCheckBox('Id Num', self)
        self.mosaic_checkbox2.stateChanged.connect(self.toggleMosaic)

        self.mosaic_checkbox3 = QCheckBox('Address', self)
        self.mosaic_checkbox3.stateChanged.connect(self.toggleMosaic)

        self.mosaic_checkbox4 = QCheckBox('FACE', self)
        self.mosaic_checkbox4.stateChanged.connect(self.toggleMosaic)

        load_button = QPushButton('Image select', self)
        load_button.clicked.connect(self.loadImage)

        hbox = QHBoxLayout()
        
        hbox.addWidget(self.image_label)

        vbox_checkboxes = QVBoxLayout()
        vbox_checkboxes.addWidget(self.mosaic_checkbox1)
        vbox_checkboxes.addWidget(self.mosaic_checkbox2)
        vbox_checkboxes.addWidget(self.mosaic_checkbox3)
        vbox_checkboxes.addWidget(self.mosaic_checkbox4)
        vbox_checkboxes.addWidget(self.result_label)

        hbox.addLayout(vbox_checkboxes)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addWidget(load_button)

        self.image_path = None
        self.original_image = None
        self.resized_image = None
        self.is_mosaic_enabled1 = False
        self.is_mosaic_enabled2 = False
        self.is_mosaic_enabled3 = False
        self.is_mosaic_enabled4 = False

        self.reader = easyocr.Reader(['ko'])  # 원하는 언어로 변경

    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png)", options=options)

        if file_name:
            self.image_path = file_name
            self.original_image = cv2.imread(self.image_path)
            self.resized_image = self.resizeImage(self.original_image)
            pixmap = self.imageToPixmap(self.resized_image)
            self.image_label.setPixmap(pixmap)

            # OpenCV로 이미지 읽기
            self.image = cv2.imread(file_name) 

            # 이미지를 불러온 후 자동으로 OCR 적용
            self.processImage()
                   
    def toggleMosaic(self, state):
        self.is_mosaic_enabled1 = self.mosaic_checkbox1.isChecked()
        self.is_mosaic_enabled2 = self.mosaic_checkbox2.isChecked()
        self.is_mosaic_enabled3 = self.mosaic_checkbox3.isChecked()
        self.is_mosaic_enabled4 = self.mosaic_checkbox4.isChecked()
        self.applyMosaic()

    def applyMosaic(self):
        if self.image_path:
            if self.is_mosaic_enabled1 or self.is_mosaic_enabled2 or self.is_mosaic_enabled3 or self.is_mosaic_enabled4:
                mosaic_image = self.resized_image.copy()
                if self.is_mosaic_enabled1:
                    mosaic_image = self.mosaicImage(mosaic_image, QRect(30, 70, 210, 35))
                if self.is_mosaic_enabled2:
                    mosaic_image = self.mosaicImage(mosaic_image, QRect(30, 105, 210, 35))
                if self.is_mosaic_enabled3:
                    mosaic_image = self.mosaicImage(mosaic_image, QRect(30, 130, 210, 50))
                if self.is_mosaic_enabled4:
                    mosaic_image = self.mosaicImage(mosaic_image, QRect(299, 59, 87, 87))

                pixmap = self.imageToPixmap(mosaic_image)
                self.image_label.setPixmap(pixmap)
            else:
                pixmap = self.imageToPixmap(self.resized_image)
                self.image_label.setPixmap(pixmap)

    def processImage(self):
        if self.image is not None:
            # 전체 이미지에 대해 EasyOCR을 적용
            results = self.reader.readtext(self.image, detail=True, paragraph=True)
            text = "\n".join([result[1] for result in results])

            # 전체 OCR 결과를 레이블에 설정
            self.result_label.setText(f":\n{text}")


    def resizeImage(self, image):
        # 이미지를 미리 리사이즈
        return cv2.resize(image, (430, 270))

    def mosaicImage(self, image, region):
        # 특정 영역에 대해 모자이크 처리
        x, y, w, h = region.x(), region.y(), region.width(), region.height()
        mosaic_region = image[y:y+h, x:x+w]
        mosaic_region = cv2.resize(mosaic_region, (w // 8, h // 8), interpolation=cv2.INTER_NEAREST)
        mosaic_region = cv2.resize(mosaic_region, (w, h), interpolation=cv2.INTER_NEAREST)

        result = image.copy()
        result[y:y+h, x:x+w] = mosaic_region

        return result

    def imageToPixmap(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(q_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageMosaicApp()
    ex.show()
    sys.exit(app.exec_())
