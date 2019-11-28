import cv2
import numpy as np 
from MTM import matchTemplates, drawBoxesOnRGB

templates = [("{}".format(i),cv2.imread('templates/{}.png'.format(i))) for i in range (10)]


def match_templates(img):
	Hits = matchTemplates(templates, img, score_threshold=0.3, N_object=4,  method=cv2.TM_CCOEFF_NORMED, maxOverlap=0.5)
	list(zip(Hits["TemplateName"], Hits["BBox"]))
	
	Overlay = drawBoxesOnRGB(img, Hits, showLabel=False)
	return Overlay, list(zip(Hits["TemplateName"], Hits["BBox"]))


