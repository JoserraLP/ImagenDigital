import sys
import os
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cvqtmanage as mng

MAX_IMG = 2

class MainWindow ():
    """ Clase principal que gestiona la interfaz de usuario
    """

    def __init__(self):
        #Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        #Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("Paso de aula")
      
        #Activar acciones de los botones 
        self.MainWindow.loadVideoButton.clicked.connect(self.loadVideo)

        #Crear los videos de Qt
        self.qt_video = [self.MainWindow.video, self.MainWindow.filter_video]
        self.cv_video = []
        
        self.video = cv2.VideoCapture()

        blue_image = np.zeros((640,480,3), np.uint8)
        blue_image[:] = (255, 0, 0)
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)


    def loadVideo(self):
        """ loadVideo se encarga de la carga del video se pulsa en el botón Load Video
        """

        self.fname, _ = QFileDialog.getOpenFileName(self.MainWindow, 'Open file', './',"Video files (*.wmv)")

        self.video = cv2.VideoCapture(self.fname)

        #Establecer el timer del filtro en ms
        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_filter.timeout.connect(self.compute)
        self.timer_filter.start(3)

        #Establecer el timer de la camara en 3 ms
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.show_frames)
        self.timer_frames.start(3)

    def show_frames(self):
        """ Convierte las imagenes de OpenCV a formato legible por Qt
            para poder visualizarlas en la interfaz
        """
        for i in range(len(self.qt_video)):
            mng.convertCV2ToQimage(self.cv_video[i],self.qt_video[i]) 
        
    def compute(self):
        self.cv_video[0] = self.video.copy()
        self.cv_video[1] = self.video.copy()
