import cv2 

class match_template():

	def __init__(self):
		self.src_img, self.template_img, self.result_mat, self.debug_img = 0, 0, 0, 0

	def readImage(self, image):
		self.src_img = cv2.imread(image)
		if (self.src_img.data == None):
			print('cv2.imread has failed loading the file')
		return self.src_img

	def readTemplate(self, image):
		self.template_img = cv2.imread(image)
		if (self.template_img.data == None):
			print('cv2.imread has failed loading the file')
		return self.template_img
	
	def convertImage(self):
		cv2.cvtColor(self.src_img, self.debug_img, cv2.CV_GRAY2BGR)
	
	def matchMethod (self, match_method ):
        # Method: CV_TM_SQDIFF, CV_TM_SQDIFF_NORMED, CV_TM _CCORR, CV_TM_CCORR_NORMED, CV_TM_CCOEFF, CV_TM_CCOEFF_NORMED
		cv2.matchTemplate(self.src_img, self.template_img, self.result_mat, match_method)
		cv2.normalize(self.result_mat, self.result_mat, 0, 1, cv2.NORM_MINMAX, -1, dtype=cv2.CV_32F)
		minVal, maxVal = 0, 0 
		minLoc, maxLoc, matchLoc = 0, 0, 0
		cv2.minMaxLoc(self.result_mat, minVal, maxVal, minLoc, maxLoc, dtype=cv2.CV_32F)
		if (match_method == cv2.CV_TM_SQDIFF or match_method == cv2.CV_TM_SQDIFF_NORMED):
			self.matchLoc = minLoc
		else:
			matchLoc = maxLoc


