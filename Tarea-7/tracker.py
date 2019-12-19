import cv2
import numpy as np
import imutils 
import matplotlib.pyplot as plt
import centroidTracker as ct
from TrackableCar import TrackableCar


class Tracker():
	""" `Tracker`
		
		Clase para realizar el proceso de tracking de vehiculos.
	"""

	def __init__(self):
		self.backSub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=50,detectShadows=False)
		self.tracker = ct.CentroidTracker(maxDisappeared=10, maxDistance=30)
		self.trackableCars = {}
	
	def roi(self,img, vertices):
		"""	`roi`
			
			Devuelve la mascara de la region de interes (ROI) calculada por los vertices

			Parameters
			----------

			- img  :  Imagen de entrada
			- vertices  :  Lista de vertices
		"""
		# mascara
		mask = np.zeros_like(img)
		# rellenamos la mascara
		cv2.fillPoly(mask, vertices, 255)
		# Mostramos solo el area que queremos
		masked = cv2.bitwise_and(img, mask)
		return masked

	def process_img(self,original_image, threshold):
		""" `process_img`

			Devuelve la imagen de entrada filtrada y le aplica el metodo MOG2

			Parameters
			----------

			- original_image  :  Imagen de entrada
			- threshold  :  Umbral para aplicar el filtro threshold
		"""
		processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
		processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
		vertices = np.array([[394,358], [337,178],
							[382,178],[464,149],
							[512,150],[638,215],
							[636,356]], np.int32)
		processed_img = self.roi(processed_img, [vertices])
		
		subtracted = self.backSub.apply(processed_img)

		_, subtracted = cv2.threshold(subtracted, threshold, 255, cv2.THRESH_BINARY)
			
		subtracted = cv2.dilate(subtracted, None, iterations=2)

		return subtracted

	def car_counter(
		self,
        img,
        threshold=150,
        bar=80,
        radio=15,
        showProcess=False):

		""" `car_counter` 
		
			Devuelve la imagen de entrada con los coches encontrados encuadrado y el contador de coches

			Parameters
			----------
			- img  :  Imagen de entrada
			- background  :  Imagen de fondo de referencia para realizar la diferencia
			- threshold  :  Umbral para descartar imagenes por debajo de este
			- bar  :  Barrera superior
			- radio :  Radio del circulo que representa el centroide
			- showProcess  :  True si se quiere mostrar todo el proceso. Por defecto, inicializada a False

			Return
			------
			- image  :  Imagen de entrada
			- contador  :  Contador de vehiculos en la imagen de entrada

		"""

		image = img.copy()

		lineThickness = 2

		output = self.process_img(image, threshold)

		contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		minarea = 400

		# area maxima de los contornos
		maxarea = 10000
		contador = 0
		
		centroids = []

		for i in range(len(contours)):

			if hierarchy[0, i, 3] == -1:  # Utilizamos la jerarquia para contar solo los contornos padres

				area = cv2.contourArea(contours[i])  # area del contorno

				if minarea < area < maxarea: # Si el area esta entre el minimo y el maximo

					# Centroides de los contornos
					cnt = contours[i]	
					x, y, w, h = cv2.boundingRect(cnt)
					cX = int((x + x+w) / 2.0)
					cY = int((y + y+h) / 2.0)

					if (cX is not 0 and cY is not 0):
						centroids.append((cX,cY))
						# Pintamos el rectangulo alrededor del contorno
						cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
						
		objects = self.tracker.update(centroids)
					
		for (objectID, centroid) in objects.items():
			
			tc = self.trackableCars.get(objectID, None)

			if tc is None:
				tc = TrackableCar(objectID,centroid)

			else:
				tc.centroids.append(centroid)
				if not tc.counted:
					if centroid[1] > bar:  # Si la ordenada del centroide supera la barrera
						contador+=1
						tc.counted = True
						cv2.circle(image, (centroid[0], centroid[1]), radio, (0, 128, 128), -1)
					
			self.trackableCars[objectID] = tc
	
		cv2.line(image, (0, bar),
				(image.shape[1], bar), (255, 255, 0), lineThickness)

		if showProcess:
			cv2.imshow("Cars Detector", output)

		return image, contador
