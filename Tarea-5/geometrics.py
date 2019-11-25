import numpy as np
import cv2
import sys
import math

class Geometrics():
    """ Gestiona la deteccion de figuras en imagenes e implementa operaciones geometricas basicas
    """

    def angle_cos(self,p0, p1, p2):
        """ Calcula el coseno que forman dos vectores generados a partir de
            tres puntos dados (p0, p1, p2)

            Parametros:
            p0 -- Primer punto
            p1 -- Segundo punto
            p2 -- Tercer punto
        """
        #Sacar los vectores que forman los tres puntos
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        #Devolver el valor absoluto de la suma de los dos vectores 
        #dividido por la raiz cuadrada del cuadrado de ambos puntos
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2)))


    def find_quadrilaterals(self,img, sigmax, sigmay, thres1, thres2, rad_aprox):
        """ Devuelve la imagen de entrada con los cuadrilateros (rectangulos y cuadrados)
            que detecta en ella contorneados, el numero de rectangulos y el numero de cuadrados.

            Parametros:
            img -- Imagen de entrada
            sigmax -- Valor de Sigma X para el filtro gaussiano
            sigmay -- Valor de Sigma Y para el filtro gaussiano
            thres1 -- Valor del thresold inferior para el filtro Canny
            thres2 -- Valor del thresold superior para el filtro Canny
            rad_approx -- Valor de aproximacion para la expresion funcional que concierne al calculo de la curva poligonal aproximada
        """

        output = img.copy()
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
                    squares.append(cnt) if self.quadrilateral_type(cnt) == "square" else rectangles.append(cnt)
        
        output = cv2.drawContours(output, rectangles, -1, (0,128,0), 3)
        output = cv2.drawContours(output, squares, -1, (128,0,0), 3)
                    
        return output, len(rectangles), len(squares)
    
    def quadrilateral_type (self, cnt):
        """ Devuelve square si cnt se corresponde con un cuadrado o
            rectangle si cnt es un rectangulo.

            Parametros:
            cnt -- Contorno de entrada
        """
        dist = lambda p1, p2: math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
        dist1 = dist(cnt[0], cnt[1])
        dist2 = dist(cnt[0], cnt[3])
        return "square" if 0 <= abs(dist1 - dist2) <= 15 else "rectangle"

    def find_circles(self, img):
        """ Devuelve la imagen de entrada con los circulos que detecta en ella
            contorneados y el numero de circulos.

            Parametros:
            img -- Imagen de entrada
        """
        output = img.copy()
        #Convertir la imagen de color BGR a gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray_blurred = cv2.blur(gray, (3, 3))
        #Sacar los circulos mediante el metodo gradiente de Hough
        #donde el tercer param es la inversa del ratio de resolucion y
        #el cuarto param es la distancia minima entre centros 
        circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=40)

        #En caso de que exista un circulo se convertira dicho circulo
        # en un int
        if circles is not None:
            circles = np.round(circles[0, :]).astype('int')
            for (x,y,r) in circles:
                cv2.circle(output, (x,y), r, (0,0,128),4)
        else:
            circles = []
        return output, len(circles)