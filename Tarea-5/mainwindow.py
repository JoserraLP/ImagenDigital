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

    valoresEsperados={
        '1':("214.2", "239.7", "195.3"),
        '2':("198.6", "206.4", "212.0"),
        '3':("190.6", "208.1", "234.6"),
        '4':("170.7", "196.6", "210.9"),
        '5':("156.2", "183.5", "178.6"),
        '6':("135.2", "162.2", "182.9"),
        '7':("167.5", "157.8", "160.9"),
        '8':("127.8", "160.0", "149.6"),
        '9':("149.8", "178.0", "146.9")
    }

    def __init__(self):
        #Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        #Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("MATCH TEMPLATE --- TAREA 2")
        self.geo = geometrics.Geometrics()
        self.MainWindow.Load_button.clicked.connect(self.getFile)
        self.MainWindow.Clip_button.clicked.connect(self.clipping)
        self.MainWindow.OCR_button.clicked.connect(self.compute)
        self.MainWindow.GLOBAL_button.clicked.connect(self.globalButton)
    
    def compute(self):
        """ Compute muestra la imagen de entrada con las figuras detectadas contorneadas
            (rectangulos, cuadrados y circulos). Ademas, muestra en pantalla el numero de
            figuras encontradas de cada tipo.
        """
        imgs_numbers = [mt.match_templates(img) for img in self.imgs]
        
        imgs_matched, list_numbers = map(list, zip(*imgs_numbers))

        list_imgs = list(map(self.resize_img, imgs_matched))
        self.MainWindow.viewer_counter1.setPixmap(list_imgs[0])
        self.MainWindow.viewer_counter2.setPixmap(list_imgs[1])
        self.MainWindow.viewer_counter3.setPixmap(list_imgs[2])

        sorted_numbers = list(map(lambda list_numb: sorted (list_numb, key= lambda number: number[1][0]), list_numbers))

        numbers = list(map(lambda str_num: tuple(map(lambda x: x[0][0], str_num)), sorted_numbers))
        
        numbers_str = tuple(map(lambda str_num: "{}{}{}.{}".format(str_num[0], str_num[1], str_num[2], str_num[3]), numbers))

        if not self.isGlobal:
            self.MainWindow.resultado1.setPlainText(numbers_str[0])
            self.MainWindow.resultado2.setPlainText(numbers_str[1])
            self.MainWindow.resultado3.setPlainText(numbers_str[2])

        with open ("salida.txt", 'a') as file:
            file.write("-----------------------------------------------------------------------\n")
            file.write("Nombre del fichero: " + self.fname + "\n")
            file.write("Contador 1: " + numbers_str[0] + " | Valor esperado: " + self.valoresEsperados[list(self.fname)[-5]][0] + "\n")
            file.write("Contador 2: " + numbers_str[1] + " | Valor esperado: " + self.valoresEsperados[list(self.fname)[-5]][1] + "\n")
            file.write("Contador 3: " + numbers_str[2] + " | Valor esperado: " + self.valoresEsperados[list(self.fname)[-5]][2] +"\n")
            file.write("-----------------------------------------------------------------------\n")

    def resize_img (self, img):
        self.resized_crop_img = cv2.resize(img, (304, 130), cv2.INTER_CUBIC) 
        cropped_img = QtGui.QImage(self.resized_crop_img, 304, 130, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(cropped_img.rgbSwapped())
        return pixmap

    def clipping(self):
        self.imgs = []
        for i in range(len(self.rectangleAreas)):
            x, y, w, h = self.rectangleAreas[i][0], self.rectangleAreas[i][1], self.rectangleAreas[i][2], self.rectangleAreas[i][3]
            
            self.crop_img = self.original_img[y:y+h, x:x+w]
            self.resized_crop_img = cv2.resize(self.crop_img, (304, 130), cv2.INTER_CUBIC)
            if not self.isGlobal:
                cropped_img = QtGui.QImage(self.resized_crop_img, 304, 130, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(cropped_img.rgbSwapped())
                if (i == 0):
                    self.MainWindow.viewer_counter1.setPixmap(pixmap)
                if (i == 1):
                    self.MainWindow.viewer_counter2.setPixmap(pixmap)
                if (i == 2):
                    self.MainWindow.viewer_counter3.setPixmap(pixmap)
            self.imgs.append(self.crop_img)


    def getFile(self):
        self.isGlobal = False
        self.fname, _ = QFileDialog.getOpenFileName(self.MainWindow, 'Open file', './',"Image files (*.jpg *.gif)")
        self.original_img = cv2.imread(self.fname, cv2.IMREAD_COLOR)
        # Cambiada de tamanio
        self.resized_img = cv2.resize(self.original_img, (720, 540), cv2.INTER_CUBIC)

        self.resized_img = self.geo.find_quadrilaterals(self.resized_img)
        
        image = QtGui.QImage(self.resized_img, 720, 540, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.MainWindow.viewer_original.setPixmap(pixmap)

    def globalButton(self):
        self.isGlobal = True
        for i in range (1,10):
            self.fname = "capturas/capturas_{}.jpg".format(i)
            self.original_img = cv2.imread("capturas/capturas_{}.jpg".format(i), cv2.IMREAD_COLOR)
            self.clipping()
            self.compute()
