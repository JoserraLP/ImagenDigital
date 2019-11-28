import sys
import os
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

    capturas = {"capturas_{}.jpg".format(i):i for i in range(1,13)} # Diccionario para tener indexadas las capturas

    valoresEsperados={
        '1':("214.2", "239.7", "195.3"),
        '2':("198.6", "206.4", "212.0"),
        '3':("190.6", "208.1", "234.6"),
        '4':("170.7", "196.6", "210.9"),
        '5':("156.2", "183.5", "178.6"),
        '6':("135.2", "162.2", "182.9"),
        '7':("167.5", "157.8", "160.9"),
        '8':("127.8", "160.0", "149.6"),
        '9':("149.8", "178.0", "146.9"),
        '10':("165.9", "169.3", "135.0"),
        '11':("157.3", "187.8", "135.0"),
        '12':("150.3", "169.3", "147.4")
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
        self.isGlobal = False
        
    
    def compute(self):
        """ Compute se encarga de realizar la extracción de los números de los contadores y de escribir estos
            números en los recuadros de la derecha
        """
        imgs_numbers = [mt.match_templates(img) for img in self.imgs] 
        
        imgs_matched, list_numbers = map(list, zip(*imgs_numbers)) # Separamos el resultado anterior en dos listas para trabajar más fácilmente

        list_imgs = list(map(self.resize_img, imgs_matched)) #Le aplicamos la funcion resize_img para que lo devuelva en formato pixmap y sea legible por Qt
        if self.isGlobal == False:
            self.MainWindow.viewer_counter1.setPixmap(list_imgs[0])
            self.MainWindow.viewer_counter2.setPixmap(list_imgs[1])
            self.MainWindow.viewer_counter3.setPixmap(list_imgs[2])

        sorted_numbers = list(map(lambda list_numb: sorted (list_numb, key= lambda number: number[1][0]), list_numbers)) # Ordenamos la lista por la primera coordenada

        numbers = list(map(lambda str_num: tuple(map(lambda x: x[0][0], str_num)), sorted_numbers)) # 
        
        numbers_str = tuple(map(lambda str_num: "{}{}{}.{}".format(str_num[0], str_num[1], str_num[2], str_num[3]), numbers)) # Pasamos a formato string los números de los contadores extraídos

        if self.isGlobal == False:
            self.MainWindow.resultado1.setPlainText(numbers_str[0])
            self.MainWindow.resultado2.setPlainText(numbers_str[1])
            self.MainWindow.resultado3.setPlainText(numbers_str[2])

        if self.isGlobal:
            with open ("salida.txt", 'a') as file:
                file.write("-----------------------------------------------------------------------\n")
                file.write("Nombre del fichero: " + self.fname + "\n")
                file.write("Contador 1: " + numbers_str[0] + " | Valor esperado: " + self.valoresEsperados[str(self.capturas[self.fname])][0] + "\n")
                file.write("Contador 2: " + numbers_str[1] + " | Valor esperado: " + self.valoresEsperados[str(self.capturas[self.fname])][1] + "\n")
                file.write("Contador 3: " + numbers_str[2] + " | Valor esperado: " + self.valoresEsperados[str(self.capturas[self.fname])][2] +"\n")
                file.write("-----------------------------------------------------------------------\n")

    def resize_img (self, img):
        """ Devuelve img en formato pixmap y le aplica resize

            Parámetros
            ----------
            - img  :  Imagen de entrada

            Return
            ------
            - pixmap : Imagen en formato pixmap, legible por Qt
        """
        self.resized_crop_img = cv2.resize(img, (304, 130), cv2.INTER_CUBIC) 
        cropped_img = QtGui.QImage(self.resized_crop_img, 304, 130, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(cropped_img.rgbSwapped())
        return pixmap

    def clipping(self):
        """ Clipping se encarga de los recortes de los contadores
        """
        self.imgs = []
        for i in range(len(self.rectangleAreas)):
            x, y, w, h = self.rectangleAreas[i][0], self.rectangleAreas[i][1], self.rectangleAreas[i][2], self.rectangleAreas[i][3]
            
            self.crop_img = self.original_img[y:y+h, x:x+w]
            self.resized_crop_img = cv2.resize(self.crop_img, (304, 130), cv2.INTER_CUBIC)
            if self.isGlobal == False:
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
        """ getFile se encarga de la carga de la captura cuando se pulsa en el botón Load Image

        """
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
        """ globalButton se encarga de escribir en un fichero de salida los resultados de todas las capturas.
        """
        open('salida.txt', 'w').close()
        self.isGlobal = True
        DIR = "capturas"
        filenames = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
        print (filenames)
        
        for name in filenames:
            self.fname = name
            self.original_img = cv2.imread("{}/{}".format(DIR, self.fname), cv2.IMREAD_COLOR)
            self.clipping()
            self.compute()
        self.isGlobal = False
        