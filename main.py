# coding:utf-8

import sys

from PyQt5.QtGui import QPixmap

import Mainwindow
import Core
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene, QMainWindow, QFileDialog, QMessageBox


class MainActivity(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.ui = Mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.picturePreview = self.ui.picturePreview
        self.selectPicture = self.ui.selectPcture

    def onSelectPictureClicked(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            self.tr(u'select the picture/video'),
            "",
            self.tr(u"images(*.png *.jpg *.jpeg *.bmp);;video files(*.avi *.mp4 *.wmv);;All files(*.*)"));
        if len(fileName) == 0:
            QMessageBox.warning(self, "Warning!", "Failed to open the media file!")
        else:
            originalScene = QGraphicsScene()
            self.picturePreview.setScene(originalScene)
            pic = QPixmap(fileName)
            originalScene.addPixmap(pic)
            self.picturePreview.show()


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myact = MainActivity()
    myact.show()
    sys.exit(myapp.exec_())
