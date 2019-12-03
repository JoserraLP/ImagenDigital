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
        self.MainWindow.startVideoButton.clicked.connect(self.startVideo)
        self.MainWindow.pauseVideoButton.clicked.connect(self.pauseVideo)

        self.velocity = self.MainWindow.velocity.value()

        #Crear los videos de Qt
        self.qt_video = [self.MainWindow.video, self.MainWindow.filter_video]
        self.cv_video = []
        
        self.video = cv2.VideoCapture()

        blue_image = np.zeros((640,480,3), np.uint8)
        blue_image[:] = (255, 0, 0)
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)

        self.MainWindow.startVideoButton.setEnabled(False)
        self.MainWindow.pauseVideoButton.setEnabled(False)

        self.MainWindow.velocity.setMinimum(3)
        self.MainWindow.velocity.setMaximum(100)
        self.MainWindow.velocity.setSingleStep(1)
        
        self.MainWindow.velocity.valueChanged.connect(self.changeVelocity)

    def loadVideo(self):
        """ loadVideo se encarga de la carga del video se pulsa en el botón Load Video
        """

        self.fname, _ = QFileDialog.getOpenFileName(self.MainWindow, 'Open file', './',"Video files (*.wmv)")

        self.video = cv2.VideoCapture(self.fname)

        #Deshabilitar boton
        self.MainWindow.loadVideoButton.setEnabled(False)
        #Habilitar botones
        self.MainWindow.startVideoButton.setEnabled(True)
        self.MainWindow.pauseVideoButton.setEnabled(True)

        self.MainWindow.video.clear()
        self.MainWindow.filter_video.clear()
        self.MainWindow.video.setText('Video cargado, haz click en "Start Video"')
        self.MainWindow.filter_video.setText('Video cargado, haz click en "Start Video"')

    def changeVelocity(self):
        self.velocity = self.MainWindow.velocity.value()
        self.MainWindow.velocity.textFromValue(self.velocity)
        self.timer_filter.start(self.velocity)
        self.timer_frames.start(self.velocity)

    def startVideo(self):
        #Establecer el timer del filtro en 50 ms
        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_filter.timeout.connect(self.compute)
        self.timer_filter.start(self.velocity)

        #Establecer el timer de la camara en 50 ms
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.show_frames)
        self.timer_frames.start(self.velocity)

    def pauseVideo(self):
        self.timer_filter.stop()
        self.timer_frames.stop()

    def resize_img(self):
        # Cambiada de tamanio
        for i in range(len(self.cv_video)):
            self.cv_video[i] = cv2.resize(self.cap.copy(), (350, 250), cv2.INTER_CUBIC)

    def show_frames(self):
        """ Convierte las imagenes de OpenCV a formato legible por Qt
            para poder visualizarlas en la interfaz
        """
        for i in range(len(self.qt_video)):
            if (self.cap is not None):
                mng.convertCV2ToQimage(self.cv_video[i],self.qt_video[i]) 

        
    def compute(self):
        #Obtener la imagen de la camara
        _, self.cap = self.video.read()
        if (self.cap is not None):
            self.cv_video[0] = self.cap.copy()
            self.cv_video[1] = self.cap.copy()
            self.resize_img()
        else:
            self.MainWindow.loadVideoButton.setEnabled(True)
            self.MainWindow.video.clear()
            self.MainWindow.filter_video.clear()
            self.MainWindow.video.setText('El video ha terminado')
            self.MainWindow.filter_video.setText('El video ha terminado')
