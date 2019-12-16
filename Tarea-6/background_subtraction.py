import cv2
import numpy as np
import imutils

""" Script para realizar la funcion `background_subtraction` a una imagen de entrada
"""

__author__      =   "Jose Ramon Lozano Pinilla, Javier Nogales Fernandez"


def background_subtraction(
        img,
        background,
        sm,
        threshold=150,
        bar1=80,
        bar2=50,
        radio=15,
        showProcess=False):

    """ `background_subtraction` 
    
        Aplica una serie de filtros y calcula la diferencia con absdiff entre background e img
        devolviendo una imagen dibujada con las barreras y el centroide y el contador de elementos.

        Parametros
        ----------
        - img  :  Imagen de entrada
        - background  :  Imagen de fondo de referencia para realizar la diferencia
        - sm  :  Maquina de estados
        - threshold  :  Umbral para descartar imagenes por debajo de este
        - bar1  :  Barrera superior
        - bar2  :  Barrera inferior
        - radio :  Radio del circulo que representa el centroide
        - showProcess  :  True si se quiere mostrar todo el proceso. Por defecto, inicializada a False

        Return
        ------
        - image  :  Imagen de entrada filtrada y dibujada con las barreras y el centroide
        - contador  :  Contador de elementos

    """

    image = img.copy()

    lineThickness = 2

    if (bar2 < bar1):
        bar1, bar2 = bar2, bar1

    first_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    first_gray = cv2.GaussianBlur(first_gray, (25, 25), 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (25, 25), 0)

    diff = cv2.absdiff(first_gray, gray)

    _, thres = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
    thres = cv2.dilate(thres, None, iterations=2)

    cnts = cv2.findContours(thres.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    contours_image = image.copy()

    M = cv2.moments(thres)

    
    cX = int(M["m10"] / (M["m00"] + 1e-5)) #calcular x del centroide
    cY = int(M["m01"] / (M["m00"] + 1e-5)) #calcular y del centroide

    if(len(cnts)!=0):
        c = max(cnts, key = cv2.contourArea)
    
        cv2.drawContours(contours_image, [c], -1, (0, 255, 0), 2)
        if (cX is not 0 and cY is not 0):
            cv2.circle(image, (cX, cY), radio, (0, 128, 128), -1)

    sm.updateBarriers(bar1, bar2)
    contador = sm.checkBarrier(cY)

        
    cv2.line(image, (0, bar1),
             (image.shape[1], bar1), (255, 255, 0), lineThickness)

    cv2.line(image, (0, bar2),
             (image.shape[1], bar2), (0, 255, 0), lineThickness)

    if showProcess:
        cv2.imshow("People Contours", contours_image)
        cv2.imshow("Background", background)
        cv2.imshow("Gray", gray)
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresh", thres)


    return image, contador
