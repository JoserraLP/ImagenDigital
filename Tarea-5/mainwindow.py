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
    def __init__(self):
        self.match_t = mt.match_template()
        #Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        #Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("MATCH TEMPLATE --- TAREA 2")
        
        self.MainWindow.Load_button.clicked.connect(self.getFile)
        
        
    
    def compute(self):
        """ Compute muestra la imagen de entrada con las figuras detectadas contorneadas
            (rectangulos, cuadrados y circulos). Ademas, muestra en pantalla el numero de
            figuras encontradas de cada tipo.
        """

    def getFile(self):
        self.fname, _= QFileDialog.getOpenFileName(self.MainWindow, 'Open file', './',"Image files (*.jpg *.gif)")
        pixmap = QPixmap(self.fname)
        self.MainWindow.viewer_original.setPixmap(pixmap)
        self.MainWindow.viewer_original.setScaledContents(True)