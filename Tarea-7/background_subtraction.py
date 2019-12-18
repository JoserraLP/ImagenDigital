import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt


""" Script para realizar la funcion `background_subtraction` a una imagen de entrada
"""

__author__      =   "Jose Ramon Lozano Pinilla, Javier Nogales Fernandez"

backSub = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=False)

def roi(img, vertices):
    # mascara
    mask = np.zeros_like(img)
    # rellenamos la mascara
    cv2.fillPoly(mask, vertices, 255)
    # Mostramos solo el area que queremos
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    vertices = np.array([[394,358], [337,178],
                        [382,178],[464,149],
                        [512,150],[638,215],
                        [636,356]], np.int32)
    processed_img = roi(processed_img, [vertices])
    
    subtracted = backSub.apply(processed_img)

    return subtracted


def background_subtraction(
        img,
        background,
        threshold=150,
        bar=80,
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
        - bar  :  Barrera superior
        - radio :  Radio del circulo que representa el centroide
        - showProcess  :  True si se quiere mostrar todo el proceso. Por defecto, inicializada a False

        Return
        ------
        - image  :  Imagen de entrada filtrada y dibujada con las barreras y el centroide
        - contador  :  Contador de elementos

    """

    image = img.copy()

    lineThickness = 2

    output = process_img(image)

    contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # area minima de los contornos
    minarea = 300

    # area maxima de los contornos
    maxarea = 10000
    contador = 0
    
    for i in range(len(contours)):

        if hierarchy[0, i, 3] == -1:  # Utilizamos la jerarquia para contar solo los contornos padres

            area = cv2.contourArea(contours[i])  # area del contorno

            if minarea < area < maxarea: # Si el area esta entre el minimo y el maximo

                # Centroides de los contornos
                cnt = contours[i]
                M = cv2.moments(cnt)
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])

                if (cX is not 0 and cY is not 0):
                    cv2.circle(image, (cX, cY), radio, (0, 128, 128), -1)
                x, y, w, h = cv2.boundingRect(cnt)
                # Pintamos el rectangulo alrededor del contorno
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    

                if bar -5 < cY < bar + 7:  # Si la ordenada del centroide supera la barrera
                    contador+=1
                    
                    
                    
    cv2.line(image, (0, bar),
            (image.shape[1], bar), (255, 255, 0), lineThickness)

    if showProcess:
        cv2.imshow("Cars Contours", output)

    return image, contador
