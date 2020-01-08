import sys
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np
import geometrics
import cvqtmanage as mng

# Camara del ordenador
IDCAM = 0
# Numero maximo de pantallas
MAX_IMG = 2


class MainWindow():
    """ Clase principal que gestiona la interfaz de usuario
    """

    def __init__(self):
        # Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        # Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("FIND CONTOURS --- TAREA 1")
        # Definir la lista de videos opencv
        self.cv_video = []
        # Definir la lista de videos en Qt (widgets TextLabel)
        self.qt_video = [self.MainWindow.cap, self.MainWindow.filter_video]

        # Obtener la camara
        self.cam = cv2.VideoCapture(IDCAM)

        blue_image = np.zeros((640, 480, 3), np.uint8)
        blue_image[:] = (255, 0, 0)
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)

        # Indicar los máximos de los diales de la interfaz a 2500 -> Se dividirá entre 1000
        self.MainWindow.sigmax_dial.setMaximum(2500)
        self.MainWindow.sigmay_dial.setMaximum(2500)

        self.MainWindow.canny_inf_dial.setMaximum(150)
        self.MainWindow.canny_sup_dial.setMaximum(150)

        self.MainWindow.rad_spin_box.setMinimum(0.01)
        self.MainWindow.rad_spin_box.setMaximum(6.28)
        self.MainWindow.rad_spin_box.setSingleStep(0.01)

        # Cambiar el valor de los LCD en funcion de los diales
        self.MainWindow.sigmax_dial.valueChanged.connect(self.change_sigmax)
        self.MainWindow.sigmay_dial.valueChanged.connect(self.change_sigmay)

        self.MainWindow.canny_inf_dial.valueChanged.connect(self.change_canny_inf)
        self.MainWindow.canny_sup_dial.valueChanged.connect(self.change_canny_sup)

        self.MainWindow.rad_spin_box.valueChanged.connect(self.change_rad_spin_box)

        # Establecer el timer del filtro en ms
        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_filter.timeout.connect(self.compute)
        self.timer_filter.start(3)

        # Establecer el timer de la camara en 3 ms
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.show_frames)
        self.timer_frames.start(3)

    def change_sigmax(self):
        """ Cambia el LCD que muestra el valor de Sigma X en funcion
            del Dial que lo regula
        """
        self.MainWindow.sigmax.display(self.MainWindow.sigmax_dial.value() / 1000)

    def change_sigmay(self):
        """ Cambia el LCD que muestra el valor de Sigma Y en funcion
            del Dial que lo regula
        """
        self.MainWindow.sigmay.display(self.MainWindow.sigmay_dial.value() / 1000)

    def change_canny_inf(self):
        """ Cambia el LCD que muestra el valor del thresold inferior
            del filtro Canny en funcion del Dial que lo regula
        """
        self.MainWindow.canny_inf.display(self.MainWindow.canny_inf_dial.value())

    def change_canny_sup(self):
        """ Cambia el LCD que muestra el valor del thresold superior
            del filtro Canny en funcion del Dial que lo regula
        """
        self.MainWindow.canny_sup.display(self.MainWindow.canny_sup_dial.value())

    def change_rad_spin_box(self):
        self.MainWindow.rad_spin_box.textFromValue(self.MainWindow.rad_spin_box.value())

    def show_frames(self):
        """ Convierte las imagenes de OpenCV a formato legible por Qt
            para poder visualizarlas en la interfaz
        """
        for i in range(len(self.qt_video)):
            mng.convertCV2ToQimage(self.cv_video[i], self.qt_video[i])

    def compute(self):
        """ Compute muestra la imagen de entrada con las figuras detectadas contorneadas
            (rectangulos, cuadrados y circulos). Ademas, muestra en pantalla el numero de
            figuras encontradas de cada tipo.
        """
        # Obtener la imagen de la camara
        _, cap = self.cam.read()

        # Pasar la imagen a cv_video[0] para que se muestre en el cuadro superior
        self.cv_video[0] = cap.copy()
        # Crear clase para ver que tipos de elementos existen
        geo = geometrics.Geometrics()
        # image será la imagen en la que se detectarán los elementos
        image = cap.copy()

        self.cv_video[1], num_circles = geo.find_circles(image)
        self.cv_video[1], num_rectangles, num_squares = geo.find_quadrilaterals(self.cv_video[1],
                                                                                self.MainWindow.sigmax_dial.value() / 1000,
                                                                                self.MainWindow.sigmay_dial.value() / 1000,
                                                                                self.MainWindow.canny_inf_dial.value(),
                                                                                self.MainWindow.canny_sup_dial.value(),
                                                                                self.MainWindow.rad_spin_box.value())

        # Cambiar el valor de los LCD en funcion del número de rectangulos, cuadrados y circulos
        self.MainWindow.num_rectangulos.display(num_rectangles)
        self.MainWindow.num_cuadrados.display(num_squares)
        self.MainWindow.num_circulos.display(num_circles)
