from PyQt5 import QtGui
import numpy as np

def convertCV2ToQimage(cv_vid,qt_vid):
    """ Convierte una imagen en formato de OpenCV (numpy array) a formato Qt
    """
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

