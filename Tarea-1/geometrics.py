import numpy as np

import cv2

import sys
import math

class Geometrics():
    """Clase para definir si un elemento es un rectangulo, cuadrado o circulo"""

    def angle_cos(self,p0, p1, p2):
        """Metodo para calcular el coseno de tres puntos"""
        #Sacar los vectores que forman los tres puntos
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        #Devolver el valor absoluto de la suma de los dos vectores 
        #dividido por la raiz cuadrada del cuadrado de ambos puntos
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2)))


    def find_quadrilaterals(self,img, sigmax, sigmay, thres1, thres2, rad_aprox):
        """Metodo para encontrar los elementos cuadrilateros: rectangulos y cuadrados"""
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Aplicar a la imagen de entrada un efecto Blur
        img = cv2.GaussianBlur(img, (5, 5), sigmax, sigmay)
        #Definir arrays para los distintos elementos
        squares, rectangles = [], []
        canny = cv2.Canny(img, thres1, thres2, apertureSize=5)
        #Devolver los contornos (Vectores de puntos) y la jerarquia de estos
        contours, _hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #Recorrer todos los contornos
        for cnt in contours:
            #Sacar el arco que forman los distintos puntos del elemento o el perimetro
            cnt_len = cv2.arcLength(cnt, True)
            #Aproximar una curva poligonal dado un porcentaje
            cnt = cv2.approxPolyDP(cnt, rad_aprox*cnt_len, True)
            #En caso de que tenga 4 puntos (lados), su area sea mayor a 1000 y sea convexo 
            #se tratará de un cuadrilatero
            if len(cnt) == 4 and cv2.contourArea(cnt) > 2000 and cv2.isContourConvex(cnt):
                #Convertir un contorno en pares de puntos
                cnt = cnt.reshape(-1, 2)
                #Calcular el coseno mayor de los distintos puntos
                max_cos = np.max([self.angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in range(4)])
                #En caso de que el coseno sea menor que 0.1 tenemos que son angulos rectos
                if max_cos < 0.1:
                    squares.append(cnt) if self.calculate_distances(cnt) == "square" else rectangles.append(cnt)
                    
        return squares, rectangles
    
    def calculate_distances (self, cnt):
        dist = lambda p1, p2: math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
        dist1 = dist(cnt[0], cnt[1])
        dist2 = dist(cnt[0], cnt[3])
        return "square" if 0 <= abs(dist1 - dist2) <= 15 else "rectangle"

    def find_circles(self, img):
        """Metodo para encontrar circulos"""
        #Convertir la imagen de color BGR a gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Sacar los circulos mediante el metodo gradiente de Hough
        #donde el tercer param es la inversa del ratio de resolucion y
        #el cuarto param es la distancia minima entre centros 
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 25)

        #En caso de que exista un circulo se convertira dicho circulo
        # en un int
        if circles is not None:
            circles = np.round(circles[0, :]).astype('int')
            return circles