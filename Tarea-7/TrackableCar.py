class TrackableCar:
	def __init__(self, objectID, centroid):
		""" `TrackableCar`
            
            Clase para controlar el trackeo sobre un coche
        """
		self.objectID = objectID
		self.centroids = [centroid]
		self.counted = False