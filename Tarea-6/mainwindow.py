import sys
import os
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cvqtmanage as mng
import background_subtraction as bs
import state_machine as sm
import time

MAX_IMG = 2


def check_video(f):
    def wrapper(*args):
        # Obtener la imagen de la camara
        _, args[0].cap = args[0].video.read()
        if (args[0].cap is not None):
            f(*args)
        else:
            args[0].MainWindow.loadVideoButton.setEnabled(True)
            args[0].MainWindow.pauseVideoButton.setEnabled(False)
            args[0].MainWindow.startVideoButton.setEnabled(False)
            args[0].MainWindow.video.clear()
            args[0].MainWindow.filter_video.clear()
            args[0].MainWindow.video.setText('El video ha terminado')
            args[0].MainWindow.filter_video.setText('El video ha terminado')
    return wrapper


class MainWindow ():
    """ Clase principal que gestiona la interfaz de usuario
    """

    def __init__(self):
        # Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        # Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("Paso de aula")

        # Activar acciones de los botones
        self.MainWindow.loadVideoButton.clicked.connect(self.loadVideo)
        self.MainWindow.startVideoButton.clicked.connect(self.startVideo)
        self.MainWindow.pauseVideoButton.clicked.connect(self.pauseVideo)
        self.MainWindow.allProcessVideo.clicked.connect(self.allProcess)
        self.MainWindow.closeAllProcessVideo.clicked.connect(self.closeAllProcess)

        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_progress = QtCore.QTimer(self.MainWindow)

        self.velocity = self.MainWindow.velocity.value()

        # Crear los videos de Qt
        self.qt_video = [self.MainWindow.video, self.MainWindow.filter_video]
        self.cv_video = []

        self.video = cv2.VideoCapture()

        blue_image = np.zeros((640, 480, 3), np.uint8)
        blue_image[:] = (255, 0, 0)
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)

        self.MainWindow.startVideoButton.setEnabled(False)
        self.MainWindow.pauseVideoButton.setEnabled(False)

        self.MainWindow.allProcessVideo.setEnabled(False)
        self.MainWindow.closeAllProcessVideo.setEnabled(False)

        self.MainWindow.velocity.setMinimum(3)
        self.MainWindow.velocity.setMaximum(100)
        self.MainWindow.velocity.setSingleStep(1)

        self.MainWindow.velocity.valueChanged.connect(self.changeVelocity)

        self.velocity = self.MainWindow.velocity.value()

        self.MainWindow.threshold.setRange(1, 255)
        self.MainWindow.threshold.setValue(70)
        self.MainWindow.threshold.setSingleStep(1)

        self.MainWindow.radio.setMinimum(5)
        self.MainWindow.radio.setMaximum(25)
        self.MainWindow.radio.setValue(15)

        self.MainWindow.radio.valueChanged.connect(self.changeCentroid)

        self.contador = 1
        self.state_machine = sm.StateMachine(cont=self.contador)

        self.show_process = False

        self.initialized = True

    def changeCentroid(self):
        self.MainWindow.radio_value.display(self.MainWindow.radio.value())

    def loadVideo(self):
        """ loadVideo se encarga de la carga del video se pulsa en el botón Load Video
        """

        self.fname, _ = QFileDialog.getOpenFileName(
            self.MainWindow, 'Open file', './', "Video files (*.wmv)")
        if self.fname:
            self.video = cv2.VideoCapture(self.fname)

            self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

            self.video_progress = 0
            
            # Deshabilitar boton
            self.MainWindow.loadVideoButton.setEnabled(False)
            # Habilitar botones
            self.MainWindow.startVideoButton.setEnabled(True)
            self.MainWindow.allProcessVideo.setEnabled(True)

            self.MainWindow.video.clear()
            self.MainWindow.filter_video.clear()
            self.MainWindow.video.setText(
                'Video cargado, haz click en "Start Video"')
            self.MainWindow.filter_video.setText(
                'Video cargado, haz click en "Start Video"')

    def changeVelocity(self):
        self.MainWindow.velocity.textFromValue(self.velocity)
        self.velocity = self.MainWindow.velocity.value()
        self.timer_filter.start(self.velocity)
        self.timer_frames.start(self.velocity)

        self.timer_progress.start(self.velocity)

    def startVideo(self):
        if (self.initialized):
            # Obtener la imagen de la camara
            _, self.cap = self.video.read()

            self.first_frame = self.cap.copy()
            self.initialized = False

        # Establecer el timer del cómputo
        self.timer_filter.timeout.connect(self.compute)
        self.timer_filter.start(self.velocity)

        # Establecer el timer de la muestra de frames
        self.timer_frames.timeout.connect(self.show_frames)
        self.timer_frames.start(self.velocity)

        #Timer para barra de progreso del video
        self.timer_progress.timeout.connect(self.progressVideo)
        self.timer_progress.start(self.velocity)

        self.MainWindow.startVideoButton.setEnabled(False)
        self.MainWindow.pauseVideoButton.setEnabled(True)

    def pauseVideo(self):
        self.timer_filter.stop()
        self.timer_frames.stop()
        self.timer_progress.stop()

        self.MainWindow.pauseVideoButton.setEnabled(False)
        self.MainWindow.startVideoButton.setEnabled(True)

    @check_video
    def show_frames(self):
        """ Convierte las imagenes de OpenCV a formato legible por Qt
            para poder visualizarlas en la interfaz
        """
        for i in range(len(self.qt_video)):
            mng.convertCV2ToQimage(self.cv_video[i], self.qt_video[i])

    @check_video
    def compute(self):
        self.cv_video[0] = self.cap.copy()

        bar1_cal = self.cv_video[0].shape[0] - int(
            (self.MainWindow.barrier1.value() / 100) * self.cv_video[0].shape[0])
        bar2_cal = self.cv_video[0].shape[0] - int(
            (self.MainWindow.barrier2.value() / 100) * self.cv_video[0].shape[0])

        self.cv_video[1], self.contador = bs.background_subtraction(self.cv_video[0], self.first_frame, sm=self.state_machine, threshold=self.MainWindow.threshold.value(
        ), bar1=bar1_cal, bar2=bar2_cal, radio=self.MainWindow.radio.value(), showProcess=self.show_process)
        self.cv_video = list(map(lambda vid: cv2.resize(
            vid, (350, 250), cv2.INTER_CUBIC), self.cv_video))

        self.MainWindow.counter.display(self.contador)

    def allProcess(self):
        self.show_process = True
        self.MainWindow.closeAllProcessVideo.setEnabled(True)
        self.MainWindow.allProcessVideo.setEnabled(False)
   
    def closeAllProcess(self):
        self.show_process = False
        cv2.destroyAllWindows()
        self.MainWindow.closeAllProcessVideo.setEnabled(False)
        self.MainWindow.allProcessVideo.setEnabled(True)
    

    def progressVideo(self):
        percentage = 200 / self.total_frames
        
        if (self.video_progress < 100):
            self.video_progress += percentage
            self.MainWindow.progressBar.setValue(int(self.video_progress))
