import sys
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np
import geometrics

#Camara del ordenador
IDCAM = 0
#Numero maximo de pantallas
MAX_IMG = 2

class Contours ():
    def __init__(self):
        #Cargar la interfaz gráfica "mainwindow.ui" en MainWindow
        self.MainWindow = uic.loadUi("mainwindow.ui")
        #Poner el titulo a la ventana MainWindow
        self.MainWindow.setWindowTitle("FIND CONTOURS --- TAREA 1")
        #Definir la lista de videos opencv
        self.cv_video=[]
        #Definir la lista de videos en Qt (widgets TextLabel)
        self.qt_video = [self.MainWindow.cap, self.MainWindow.filter_video]

        #Obtener la camara
        self.cam = cv2.VideoCapture(IDCAM)

        #Añadir imagenes azules para activar la imagen de la pantalla
        blue_image = np.zeros((640,480,3), np.uint8)
        blue_image[:] = (255, 0, 0) #ojo bgr
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)

        #Indicar los máximos de los diales de la interfaz a 2500 -> Se dividirá entre 1000
        self.MainWindow.sigmax_dial.setMaximum(2500)
        self.MainWindow.sigmay_dial.setMaximum(2500)

        self.MainWindow.canny_inf_dial.setMaximum(150)
        self.MainWindow.canny_sup_dial.setMaximum(150)

        #Cambiar el valor de los LCD en funcion de los diales
        self.MainWindow.sigmax_dial.valueChanged.connect(self.change_sigmax)
        self.MainWindow.sigmay_dial.valueChanged.connect(self.change_sigmay)
        
        self.MainWindow.canny_inf_dial.valueChanged.connect(self.change_canny_inf)
        self.MainWindow.canny_sup_dial.valueChanged.connect(self.change_canny_sup)

        #Establecer el timer del filtro en ms
        self.timer_filter = QtCore.QTimer(self.MainWindow)
        self.timer_filter.timeout.connect(self.make_contour)
        self.timer_filter.start(3)

        #Establecer el timer de la camara en 3 ms
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.show_frames)
        self.timer_frames.start(3)

    def change_sigmax(self):
        self.MainWindow.sigmax.display(self.MainWindow.sigmax_dial.value()/1000) 

    def change_sigmay(self):
        self.MainWindow.sigmay.display(self.MainWindow.sigmay_dial.value()/1000)

    def change_canny_inf(self):
        self.MainWindow.canny_inf.display(self.MainWindow.canny_inf_dial.value())

    def change_canny_sup(self):
        self.MainWindow.canny_sup.display(self.MainWindow.canny_sup_dial.value())

    def make_contour(self):
        """Metodo para realizar los contornos alrededor del elemento detectado"""
        #Obtener la imagen de la carama
        _, cap = self.cam.read()
        #Pasar la imagen a cv_video[0] para que se muestre en el cuadro superior
        self.cv_video[0] = cap.copy()
        #Crear clase para ver que tipos de elementos existen
        geo = geometrics.Geometrics()
        #image será la imagen en la que se detectarán los elementos
        image = cap.copy ()
        #output será la imagen en la que se dibujarán los elementos
        output = cap.copy()
        #Sacar los cuadrados y rectángulos de la imagen de entrada
        squares, rectangles = geo.find_quadrilaterals(image)
        #Sacar los circulos de la imagen de entrada
        circles = geo.find_circles(image)

        #Pasar la imagen a cv_video[1] para que se muestre en el cuadro inferior
        #Cada elemento tendrá un color distinto
        #Rectangulo: verde, Cuadrado: azul, Circulo: rojo
        self.cv_video[1] = output
        self.cv_video[1] = cv2.drawContours(self.cv_video[1], rectangles, -1, (0,128,0), 3)
        self.cv_video[1] = cv2.drawContours(self.cv_video[1], squares, -1, (128,0,0), 3)

        if circles is not None:
            for (x,y,r) in circles:
                cv2.circle(self.cv_video[1], (x,y), r, (0,0,128), 4)
        else:
            circles = []

        #Cambiar el valor de los LCD en funcion del número de rectangulos, cuadrados y circulos
        self.MainWindow.num_rectangulos.display(len(rectangles))
        self.MainWindow.num_cuadrados.display(len(squares))
        self.MainWindow.num_circulos.display(len(circles))

    def convertCV2ToQimage(self,cv_vid,qt_vid):
        gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]
        if cv_vid is None:
            return
        if cv_vid.dtype!=np.uint8:
            return
        if len(cv_vid.shape)==2:
            image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_Indexed8)
            image.setColorTable(gray_color_table)
        if len(cv_vid.shape)==3:
            if cv_vid.shape[2]==3:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_RGB888)
            elif cv_vid.shape[2]==4:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        qt_vid.setPixmap(pixmap)

    def show_frames(self):
        """Método para mostrar las distintas imagenes en los cuadros"""
        for i in range(len(self.qt_video)):
            self.convertCV2ToQimage(self.cv_video[i],self.qt_video[i])       
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Contours()
    w.MainWindow.show()
    app.exec_()
