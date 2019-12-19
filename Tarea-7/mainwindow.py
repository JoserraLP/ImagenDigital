import sys
import os
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cvqtmanage as mng
import tracker as t

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
        _, args[0].cap = args[0].video.read()  # Obtener la imagen de la camara
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

        # Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        # Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("Contador de coches en autovia")

        # Activar acciones de los botones
        self.MainWindow.loadVideoButton.clicked.connect(self.loadVideo)
        self.MainWindow.startVideoButton.clicked.connect(self.startVideo)
        self.MainWindow.pauseVideoButton.clicked.connect(self.pauseVideo)
        self.MainWindow.allProcessVideo.clicked.connect(self.allProcess)
        self.MainWindow.closeAllProcessVideo.clicked.connect(self.closeAllProcess)
        self.MainWindow.velocity.valueChanged.connect(self.changeVelocity)

        # Establecer los timers
        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_progress = QtCore.QTimer(self.MainWindow)

        # Crear los videos de Qt
        self.qt_video = [self.MainWindow.video, self.MainWindow.filter_video]
        self.cv_video = []

        self.tracker = t.Tracker()

        # Capturar el video
        self.video = cv2.VideoCapture()

        # Convertir el video en azul para que cargue correctamente
        blue_image = np.zeros((640, 480, 3), np.uint8)
        blue_image[:] = (255, 0, 0)
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)

        # Activar/Desactivar botones
        self.MainWindow.startVideoButton.setEnabled(False)
        self.MainWindow.pauseVideoButton.setEnabled(False)
        self.MainWindow.allProcessVideo.setEnabled(False)
        self.MainWindow.closeAllProcessVideo.setEnabled(False)
        self.MainWindow.velocity.setEnabled(False)
        self.MainWindow.threshold.setEnabled(False)

        # Valores de threshold
        self.MainWindow.threshold.setRange(1, 255)
        self.MainWindow.threshold.setValue(70)
        self.MainWindow.threshold.setSingleStep(1)

        # Valores de la velocidad
        self.MainWindow.velocity.setMinimum(3)
        self.MainWindow.velocity.setMaximum(100)
        self.MainWindow.velocity.setSingleStep(1)

        self.velocity = self.MainWindow.velocity.value()

        # Establecer variables globales
        self.contador = 0

        self.show_process = False

        self.initialized = True

    def loadVideo(self):
        """ `loadVideo`

            Callback encargado de la carga del vide cuando se pulsa en el botón Load Video
        """

        # Abrir cuadro de dialogo para seleccionar fichero
        self.fname, _ = QFileDialog.getOpenFileName(
            self.MainWindow, 'Open file', './', "Video files (*.wmv, *mp4)")
        if self.fname:
            # Obtener el video del fichero seleccionado
            self.video = cv2.VideoCapture(self.fname)

            # Establecer el contador
            self.contador = 0

            # Calcular el número total de frames
            self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

            # Reiniciar los valores del progreso y el timer del progeso
            self.video_progress = 0
            self.timer_progress.stop()

            # Activar/Desactivar botones
            self.MainWindow.loadVideoButton.setEnabled(False)
            self.MainWindow.startVideoButton.setEnabled(True)

            # Limpieza de la interfaz
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

        # Obtener el valor de la velocidad
        self.MainWindow.velocity.textFromValue(self.velocity)
        self.velocity = self.MainWindow.velocity.value()

        # Iniciar los timers al valor de la velocidad actual
        self.timer_filter.start(self.velocity)
        self.timer_frames.start(self.velocity)
        self.timer_progress.start(self.velocity)

    def startVideo(self):
        """ `startVideo`
            
            Callback enlazado con el boton Start Video para gestionar la reanudacion y comienzo
            del video
        """
        self.velocity = 99
        # Establecer el timer del cómputo
        self.timer_filter.timeout.connect(self.compute)
        self.timer_filter.start(self.velocity)

        # Establecer el timer de la muestra de frames
        self.timer_frames.timeout.connect(self.show_frames)
        self.timer_frames.start(self.velocity)

        # Timer para barra de progreso del video
        self.timer_progress.timeout.connect(self.progressVideo)
        self.timer_progress.start(self.velocity)

        # Activar/Desactivar botones
        self.MainWindow.velocity.setEnabled(True)
        self.MainWindow.threshold.setEnabled(True)
        self.MainWindow.allProcessVideo.setEnabled(True)
        self.MainWindow.startVideoButton.setEnabled(False)
        self.MainWindow.pauseVideoButton.setEnabled(True)

    def pauseVideo(self):
        """ `pauseVideo`
            
            Callback enlazado con el boton de Pausa del video
        """

        # Parar todos los timer
        self.timer_filter.stop()
        self.timer_frames.stop()
        self.timer_progress.stop()

        # Activar/Desactivar botones
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

        # Obtener una copia del video
        self.cv_video[0] = self.cap.copy()

        # Cálculo de la barrera
        bar_cal = self.cv_video[0].shape[0] - int(
            (self.MainWindow.barrier.value() / 100) * self.cv_video[0].shape[0])

        # Devolver la imagen procesada y el contador de coches
        self.cv_video[1], add = self.tracker.car_counter(self.cv_video[0], threshold=self.MainWindow.threshold.value(), bar=bar_cal, showProcess=self.show_process)
        self.cv_video = list(map(lambda vid: cv2.resize(vid, (350, 250), cv2.INTER_CUBIC), self.cv_video))
        
        self.contador +=add

        # Mostrar el valor del contador en el LCD
        self.MainWindow.counter.display(self.contador)

    def allProcess(self):
        """ `allProcess`
        
            Callback del boton Watch All Process
        """

        # Activar la bandera para mostrar el proceso
        self.show_process = True

        # Activar/Desactivar botones
        self.MainWindow.closeAllProcessVideo.setEnabled(True)
        self.MainWindow.allProcessVideo.setEnabled(False)
   
    def closeAllProcess(self):
        """ `closeAllProcess`
            
            Callback del boton Close All Process
        """

        # Desactivar la bandera
        self.show_process = False

        # Cerrar todas las ventanas
        cv2.destroyAllWindows()

        # Activar/Desactivar botones
        self.MainWindow.closeAllProcessVideo.setEnabled(False)
        self.MainWindow.allProcessVideo.setEnabled(True)

    def progressVideo(self):
        """ `progressVideo`
            
            Callback que actualiza la ProgressBar de la GUI
        """

        # Calcular el porcentaje, 200 porque se toman dos frames
        percentage = 200 / self.total_frames

        # Actualizar el valor del progreso
        if (self.video_progress < 100):
            self.video_progress += percentage
            self.MainWindow.progressBar.setValue(int(self.video_progress))