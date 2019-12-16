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

MAX_IMG = 2

__author__      =   "Jose Ramon Lozano Pinilla, Javier Nogales Fernandez"

def check_video(f):
    """ `check_video` 

        Decorador que controla que el video se este reproduciendo. Si ha terminado
        de reproducirse, habilita y deshabilita los botones de la GUI correctamente y muestra los 
        mensajes de fin de video

        Parametros
        ----------
        - f  :  Funcion a decorar
    """
    def wrapper(*args):
        _, args[0].cap = args[0].video.read() # Obtener la imagen de la camara
        if (args[0].cap is not None):
            f(*args)
        else:
            args[0].MainWindow.loadVideoButton.setEnabled(True) #Habilitamos el boton LoadVideo
            args[0].MainWindow.pauseVideoButton.setEnabled(False) #Inhabilitamos el boton PauseVideo
            args[0].MainWindow.startVideoButton.setEnabled(False) #Inhabilitamos el boton StarVideo
            args[0].MainWindow.allProcessVideo.setEnabled(False) #Inhabilitamos el boton Watch All Proccess
            args[0].MainWindow.video.clear() #Limpiamos la pantalla del video original
            args[0].MainWindow.filter_video.clear() #Limpiamos la pantalla del video con el filtro aplicado
            args[0].MainWindow.video.setText('El video ha terminado')
            args[0].MainWindow.filter_video.setText('El video ha terminado')
            args[0].timer_filter.stop() #Paramos el timer del video filtrado
            args[0].timer_frames.stop() #Paramos el timer del video original
    return wrapper


class MainWindow ():
    """ `MainWindow`
        
        Clase principal que gestiona la interfaz de usuario
    """

    def __init__(self):
        """ `__init__`
        
            Inicia la clase `MainWindow`. Para mas info utilizar::
                $ help(MainWindow)
        """

        
        self.MainWindow = uic.loadUi("mainwindow.ui") # Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        
        self.MainWindow.setWindowTitle("Paso de aula") # Poner el titulo a la ventana MainWindow

        self.MainWindow.loadVideoButton.clicked.connect(self.loadVideo)
        self.MainWindow.startVideoButton.clicked.connect(self.startVideo)
        self.MainWindow.pauseVideoButton.clicked.connect(self.pauseVideo)
        self.MainWindow.allProcessVideo.clicked.connect(self.allProcess)
        self.MainWindow.closeAllProcessVideo.clicked.connect(self.closeAllProcess)

        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_progress = QtCore.QTimer(self.MainWindow)

        self.velocity = self.MainWindow.velocity.value()

        
        self.qt_video = [self.MainWindow.video, self.MainWindow.filter_video] # Crear los videos de Qt
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

        self.MainWindow.velocity.setEnabled(False)

        self.MainWindow.threshold.setEnabled(False)

        self.MainWindow.velocity.setMinimum(3)
        self.MainWindow.velocity.setMaximum(100)
        self.MainWindow.velocity.setSingleStep(1)

        self.MainWindow.velocity.valueChanged.connect(self.changeVelocity)

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
        """ `changeCentroid`
            
            Callback encargado de cambiar el  LCD que muestra el radio del circulo que
            representa el centroide
        """

        self.MainWindow.radio_value.display(self.MainWindow.radio.value())

    def loadVideo(self):
        """ `loadVideo`

            Callback encargado de la carga del vide cuando se pulsa en el botón Load Video
        """
        self.fname, _ = QFileDialog.getOpenFileName(
            self.MainWindow, 'Open file', './', "Video files (*.wmv)")
        if self.fname:
            self.video = cv2.VideoCapture(self.fname)

            self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            self.contador = 1
            self.video_progress = 0
            self.timer_progress.stop()

            
            self.MainWindow.loadVideoButton.setEnabled(False) # Deshabilitar boton
            
            self.MainWindow.startVideoButton.setEnabled(True) # Habilitar botones

            self.MainWindow.video.clear()
            self.MainWindow.filter_video.clear()
            self.MainWindow.video.setText(
                'Video cargado, haz click en "Start Video"')
            self.MainWindow.filter_video.setText(
                'Video cargado, haz click en "Start Video"')

    def changeVelocity(self):
        """ `changeVelocity`
            
            Callback conectado al SpinBox que modifica la velocidad. Restablece los timers
            con la nueva velocidad de refresco
        """
        self.MainWindow.velocity.textFromValue(self.velocity)
        self.velocity = self.MainWindow.velocity.value()
        self.timer_filter.start(self.velocity)
        self.timer_frames.start(self.velocity)

        self.timer_progress.start(self.velocity)

    def startVideo(self):
        """ `startVideo`
            
            Callback enlazado con el boton Start Video para gestionar la reanudacion y comienzo
            del video
        """
        if (self.initialized):
            _, self.cap = self.video.read() #  Obtener la imagen de la camara

            self.first_frame = self.cap.copy()
            self.initialized = False
        
        self.MainWindow.velocity.setEnabled(True)

        self.MainWindow.threshold.setEnabled(True)

        self.MainWindow.allProcessVideo.setEnabled(True)

        
        self.timer_filter.timeout.connect(self.compute) # Establecer el timer del cómputo
        self.timer_filter.start(self.velocity)

        
        self.timer_frames.timeout.connect(self.show_frames) # Establecer el timer de la muestra de frames
        self.timer_frames.start(self.velocity)

        
        self.timer_progress.timeout.connect(self.progressVideo) #Timer para barra de progreso del video
        self.timer_progress.start(self.velocity)


        self.MainWindow.startVideoButton.setEnabled(False)
        self.MainWindow.pauseVideoButton.setEnabled(True)

    def pauseVideo(self):
        """ `pauseVideo`
            
            Callback enlazado con el boton de Pausa del video
        """
        self.timer_filter.stop()
        self.timer_frames.stop()
        self.timer_progress.stop()

        self.MainWindow.pauseVideoButton.setEnabled(False)
        self.MainWindow.startVideoButton.setEnabled(True)

    @check_video
    def show_frames(self):
        """ `show_frames`
            
            Convierte las imagenes de OpenCV a formato legible por Qt
            para poder visualizarlas en la interfaz
        """
        for i in range(len(self.qt_video)):
            mng.convertCV2ToQimage(self.cv_video[i], self.qt_video[i])

    @check_video
    def compute(self):
        """ `compute`
        
            Callback que realiza el cálculo de las ordenadas de las barreras,
            aplica background_subtraction al frame actual, aplica resize al frame
            para adaptarlo a la GUI y actualiza el contador.
        """

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
        """ `allProcess`
        
            Callback del boton Watch All Process
        """
        self.show_process = True
        self.MainWindow.closeAllProcessVideo.setEnabled(True)
        self.MainWindow.allProcessVideo.setEnabled(False)
   
    def closeAllProcess(self):
        """ `closeAllProcess`
            
            Callback del boton Close All Process
        """
        self.show_process = False
        cv2.destroyAllWindows()
        self.MainWindow.closeAllProcessVideo.setEnabled(False)
        self.MainWindow.allProcessVideo.setEnabled(True)
    

    def progressVideo(self):
        """ `progressVideo`
            
            Callback que actualiza la ProgressBar de la GUI
        """

        percentage = 200 / self.total_frames
        
        if (self.video_progress < 100):
            self.video_progress += percentage
            self.MainWindow.progressBar.setValue(int(self.video_progress))
