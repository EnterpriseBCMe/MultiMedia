# coding:utf-8

import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMainWindow, QFileDialog, QMessageBox

import Mainwindow
import Core


class MainActivity(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.ui = Mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.picturePreview = self.ui.picturePreview
        self.watermarkPreview = self.ui.watermarkPreview
        self.selectPicture = self.ui.selectPicture
        self.selectWatermark = self.ui.selectWatermark
        self.pictureName = ''
        self.watermarkName = ''

    def onSelectPictureClicked(self):
        self.pictureName, _ = QFileDialog.getOpenFileName(
            self,
            self.tr(u'select the picture/video'),
            "",
            self.tr(u"images(*.png *.jpg *.jpeg *.bmp);;video files(*.avi *.mp4 *.wmv);;All files(*.*)"))
        if len(self.pictureName) == 0:
            QMessageBox.warning(self, "Warning!", "Failed to open the media file!")
        else:
            originalScene = QGraphicsScene()
            self.picturePreview.setScene(originalScene)
            pic = QPixmap(self.pictureName)
            originalScene.addPixmap(pic)
            self.picturePreview.show()

    def onSelectWatermarkClicked(self):
        self.watermarkName, _ = QFileDialog.getOpenFileName(
            self,
            self.tr(u'select the watermark'),
            "",
            self.tr(u"images(*.png *.jpg *.jpeg *.bmp)"))
        if len(self.watermarkName) == 0:
            QMessageBox.warning(self, "Warning!", "Failed to open the watermark file!")
        else:
            originalScene = QGraphicsScene()
            self.watermarkPreview.setScene(originalScene)
            pic = QPixmap(self.watermarkName)
            originalScene.addPixmap(pic)
            self.watermarkPreview.show()

    def onWatermarkClicked(self):
        if len(self.pictureName) == 0 or len(self.watermarkName) == 0:
            QMessageBox.warning(self, "Warning!", "Failed to open the picture or watermark!")
        Core.watermarking(self.pictureName, self.watermarkName)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myact = MainActivity()
    myact.show()
    sys.exit(myapp.exec_())
