import sys
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np

IDCAM = 0
MAX_IMG = 2

class Contours ():
    def __init__(self):
        self.MainWindow = uic.loadUi("mainwindow.ui")
        self.MainWindow.setWindowTitle("FIND CONTOURS --- TAREA 1")
        self.cv_video=[]
        self.qt_video = [self.MainWindow.cap, self.MainWindow.filter_video]

        self.cam = cv2.VideoCapture(IDCAM)

        blue_image = np.zeros((640,480,3), np.uint8)
        blue_image[:] = (255, 0, 0) #ojo bgr
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)

        self.MainWindow.sigmax_dial.setMaximum(150)
        self.MainWindow.sigmay_dial.setMaximum(150)

        self.MainWindow.canny_inf_dial.setMaximum(150)
        self.MainWindow.canny_sup_dial.setMaximum(150)

        self.MainWindow.sigmax_dial.valueChanged.connect(self.change_sigmax)
        self.MainWindow.sigmay_dial.valueChanged.connect(self.change_sigmay)
        
        self.MainWindow.canny_inf_dial.valueChanged.connect(self.change_canny_inf)
        self.MainWindow.canny_sup_dial.valueChanged.connect(self.change_canny_sup)

        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_filter.timeout.connect(self.make_contour)

        self.timer_filter.start(3)

        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.show_frames)
        self.timer_frames.start(3)

    def change_sigmax(self):
        self.MainWindow.sigmax.display(self.MainWindow.sigmax_dial.value()) 

    def change_sigmay(self):
        self.MainWindow.sigmay.display(self.MainWindow.sigmay_dial.value())

    def change_canny_inf(self):
        self.MainWindow.canny_inf.display(self.MainWindow.canny_inf_dial.value())

    def change_canny_sup(self):
        self.MainWindow.canny_sup.display(self.MainWindow.canny_sup_dial.value())

    def convertCV2ToQimage(self,cv_vid,qt_vid):
        gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]
        if cv_vid is None:
            return
        if cv_vid.dtype!=np.uint8:
            return
        if len(cv_vid.shape)==2:
            image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_Indexed8)
            image.setColorTable(gray_color_table)
        if len(cv_vid.shape)==3:
            if cv_vid.shape[2]==3:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_RGB888)
            elif cv_vid.shape[2]==4:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        qt_vid.setPixmap(pixmap)

    def make_contour(self):
        _, cap = self.cam.read()
        self.height, self.width = cap.shape[:2]
        self.cv_video[0] = cap.copy()
        self.cv_video[1] = cv2.GaussianBlur(self.cv_video[0], (5,5), sigmaX = self.MainWindow.sigmax.value(), sigmaY = self.MainWindow.sigmay.value())
        


    def show_frames(self):
        for i in range(len(self.qt_video)):
            self.convertCV2ToQimage(self.cv_video[i],self.qt_video[i])       
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Contours()
    w.MainWindow.show()
    app.exec_()
