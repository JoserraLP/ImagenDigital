import sys
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import geometrics
import cvqtmanage as mng
import match_template as mt

class MainWindow ():
    """ Clase principal que gestiona la interfaz de usuario
    """

    rectangleAreas=[
        (1030,564,400,140),
        (1030,850,400,140),
        (1030,1144,400,140)
    ]

    def __init__(self):
        self.match_t = mt.match_template()
        #Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        #Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("MATCH TEMPLATE --- TAREA 2")
        self.geo = geometrics.Geometrics()
        self.MainWindow.Load_button.clicked.connect(self.getFile)
        self.MainWindow.Clip_button.clicked.connect(self.clipping)
        self.MainWindow.OCR_button.clicked.connect(self.compute)
       
    
    def compute(self):
        """ Compute muestra la imagen de entrada con las figuras detectadas contorneadas
            (rectangulos, cuadrados y circulos). Ademas, muestra en pantalla el numero de
            figuras encontradas de cada tipo.
        """
        pass


    def clipping(self):
        for i in range(len(self.rectangleAreas)):
            x, y, w, h = self.rectangleAreas[i][0], self.rectangleAreas[i][1], self.rectangleAreas[i][2], self.rectangleAreas[i][3]
            
            self.crop_img = self.original_img[y:y+h, x:x+w]
            self.resized_crop_img = cv2.resize(self.crop_img, (304, 130), cv2.INTER_CUBIC)
            
            cropped_img = QtGui.QImage(self.resized_crop_img, 304, 130, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(cropped_img.rgbSwapped())
            if (i == 0):
                self.MainWindow.viewer_counter1.setPixmap(pixmap)
            if (i == 1):
                self.MainWindow.viewer_counter2.setPixmap(pixmap)
            if (i == 2):
	            self.MainWindow.viewer_counter3.setPixmap(pixmap)
        


    def getFile(self):
        self.fname, _ = QFileDialog.getOpenFileName(self.MainWindow, 'Open file', './',"Image files (*.jpg *.gif)")
        self.original_img = cv2.imread(self.fname, cv2.IMREAD_COLOR)
        # Cambiada de tamanio
        self.resized_img = cv2.resize(self.original_img, (720, 540), cv2.INTER_CUBIC)

        self.resized_img = self.geo.find_quadrilaterals(self.resized_img)
        
        image = QtGui.QImage(self.resized_img, 720, 540, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.MainWindow.viewer_original.setPixmap(pixmap)