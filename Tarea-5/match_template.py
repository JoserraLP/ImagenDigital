import cv2
import numpy as np 
from MTM import matchTemplates, drawBoxesOnRGB


templates = [("{}".format(i),cv2.imread('templates/{}.png'.format(i))) for i in range (10)] #Cargamos todos los templates


def match_templates(img):
	""" 
	Devuelve la imagen con los templates encuadrados y una lista que contiene tuplas con el nombre del
	template y las coordenadas del rectángulo

	Parámetros
	----------
	- img  :  Imagen de entrada

	Return
	------
	- Overlay  :  imagen original con los templates encuadrados
	- list_templates  :  Lista que contiene tuplas con (nombre del template, coordenadas del rectangulo)
	"""
	Hits = matchTemplates(templates, img, score_threshold=0.3, N_object=4, method=cv2.TM_CCOEFF_NORMED, maxOverlap=0.4)	
	list_templates = list(zip(Hits["TemplateName"], Hits["BBox"]))
	Overlay = drawBoxesOnRGB(img, Hits, showLabel=False)
	return Overlay, list_templates
