import numpy as np

import cv2

import sys


class Geometrics():
    """Clase para definir si un elemento es un rectangulo, cuadrado o circulo"""

    def angle_cos(self,p0, p1, p2):
        """Metodo para calcular el coseno de tres puntos"""
        #Sacar los vectores que forman los tres puntos
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        #Devolver el valor absoluto de la suma de los dos vectores 
        #dividido por la raiz cuadrada del cuadrado de ambos puntos
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2)))


    def find_quadrilaterals(self,img):
        """Metodo para encontrar los elementos cuadrilateros: rectangulos y cuadrados"""
        #Aplicar a la imagen de entrada un efecto Blur
        img = cv2.GaussianBlur(img, (5, 5), 0)
        #Definir arrays para los distintos elementos
        squares, rectangles = [], []
        for gray in cv2.split(img):
            for thrs in range(0, 255, 26):
                if thrs == 0:
                    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                    bin = cv2.dilate(bin, None)
                else:
                    _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                #Devolver los contornos (Vectores de puntos) y la jerarquia de estos
                contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                #Recorrer todos los contornos
                for cnt in contours:
                    #Sacar el arco que forman los distintos puntos del elemento o el perimetro
                    cnt_len = cv2.arcLength(cnt, True)
                    #Aproximar una curva poligonal dado un porcentaje (segundo parametro)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    #En caso de que tenga 4 puntos (lados), su area sea mayor a 1000 y sea convexo 
                    #se tratará de un cuadrilatero
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                        #Convertir un contorno en pares de puntos
                        cnt = cnt.reshape(-1, 2)
                        #Calcular el coseno mayor de los distintos puntos
                        max_cos = np.max([self.angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in range(4)])
                        #En caso de que el coseno sea menor que 0.1 tenemos que son angulos rectos
                        if max_cos < 0.1:
                            #Calcular el rectangulo superior derecho del contorno
                            (x, y, w, h) = cv2.boundingRect(cnt)
                            #Sacamos el radio de aspecto del cuadrilatero
                            ar = w / float(h)
 
                            # un cuadrado tendrá una relación de aspecto que es aproximadamente
                            # igual a uno, de lo contrario, la forma es un rectángulo
                            squares.append(cnt) if ar >= 0.95 and ar <= 1.05 else rectangles.append(cnt)
                            
                        return squares, rectangles

    def find_circles(self, img):
        """Metodo para encontrar circulos"""
        #Convertir la imagen de color BGR a gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Sacar los circulos mediante el metodo gradiente de Hough
        #donde el tercer param es la inversa del ratio de resolucion y
        #el cuarto param es la distancia minima entre centros 
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 25)

        #En caso de que exista un circulo se convertira dicho 
        if circles is not None:
            circles = np.round(circles[0, :]).astype('int')
            return circles




        

 
        
        



