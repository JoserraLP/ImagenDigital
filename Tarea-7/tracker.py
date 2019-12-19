import cv2
import numpy as np
import imutils 
import matplotlib.pyplot as plt
import centroidTracker as ct
from TrackableCar import TrackableCar


class Tracker():

	def __init__(self):
		self.backSub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=50,detectShadows=False)
		self.tracker = ct.CentroidTracker(maxDisappeared=10, maxDistance=30)
		self.trackableCars = {}
		self.carsClassifier = cv2.CascadeClassifier('cars.xml')

	
	def roi(self,img, vertices):
		# mascara
		mask = np.zeros_like(img)
		# rellenamos la mascara
		cv2.fillPoly(mask, vertices, 255)
		# Mostramos solo el area que queremos
		masked = cv2.bitwise_and(img, mask)
		return masked

	def process_img(self,original_image, threshold):
		processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
		#processed_img = cv2.GaussianBlur(processed_img, (11, 11), 0)
		vertices = np.array([[394,358], [337,178],
							[382,178],[464,149],
							[512,150],[638,215],
							[636,356]], np.int32)
		processed_img = self.roi(processed_img, [vertices])
		
		subtracted = self.backSub.apply(processed_img)
		"""
		_, thres = cv2.threshold(subtracted, threshold, 255, cv2.THRESH_BINARY)
			
		thres = cv2.dilate(thres, None, iterations=2)
		
		cnts = cv2.findContours(thres.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		contours_image = original_image.copy()

		if(len(cnts)!=0):
			c = max(cnts, key = cv2.contourArea)
		
			M = cv2.moments(c)
			cX = int(M['m10'] / M['m00'])
			cY = int(M['m01'] / M['m00'])
			cv2.drawContours(contours_image, [c], -1, (0, 255, 0), 2)

			if (cX is not 0 and cY is not 0):
				cv2.circle(contours_image, (cX, cY), 1, (0, 128, 128), -1)
			x, y, w, h = cv2.boundingRect(c)
			# Pintamos el rectangulo alrededor del contorno
			cv2.rectangle(contours_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

		cv2.imshow("Test", contours_image)
		"""

		return subtracted

	def background_subtraction(
		self,
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

		if neural == False:

			output = self.process_img(image, threshold)

			contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			
			# area minima de los contornos
			#minarea = 300*0.0050*bar
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
						M = cv2.moments(cnt)
						#cX = int(M['m10'] / M['m00'])
						#cY = int(M['m01'] / M['m00'])
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
							text ="ID {}".format(objectID)
							print(text)
						
				self.trackableCars[objectID] = tc

		else:
			pass
		
						
						
		cv2.line(image, (0, bar),
				(image.shape[1], bar), (255, 255, 0), lineThickness)

		if showProcess:
			cv2.imshow("Cars Detector", output)

		return image, contador
