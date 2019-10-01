import numpy as np

import cv2

import sys


class Geometrics():

    def angle_cos(self,p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2)))


    def find_quadrilaterals(self,img):
        img = cv2.GaussianBlur(img, (5, 5), 0)
        squares = []
        rectangles = []
        for gray in cv2.split(img):
            for thrs in range(0, 255, 26):
                if thrs == 0:
                    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                    bin = cv2.dilate(bin, None)
                else:
                    _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([self.angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                        if max_cos < 0.1:
                            (x, y, w, h) = cv2.boundingRect(cnt)
                            ar = w / float(h)
 
                            # a square will have an aspect ratio that is approximately
                            # equal to one, otherwise, the shape is a rectangle
                            squares.append(cnt) if ar >= 0.95 and ar <= 1.05 else rectangles.append(cnt)
                            
        return squares, rectangles

    def circles(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

        if circles is not None:
            circles = np.round(circles[0, :]).astype('int')
            return circles




        

 
        
        



