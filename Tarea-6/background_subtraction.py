import cv2
import numpy as np 

def background_subtraction(img, background, threshold =150, bar1=50, bar2=80):
    
    image = img.copy()
    
    lineThickness = 2
    

    cv2.line(image, (0, bar1), (image.shape[1], bar1), (255,255,0), lineThickness)

    cv2.line(image, (0, bar2), (image.shape[1], bar2), (0,255,0), lineThickness)

    if (bar2 < bar1):
        bar1, bar2 = bar2, bar1

    first_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    first_gray = cv2.GaussianBlur(first_gray, (25, 25), 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (25,25), 0)

    diff = cv2.absdiff(first_gray, gray)
 
    _,thres = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    
    thres = cv2.dilate(thres, None, iterations=2)

    M = cv2.moments(thres)
 
    # calculate x,y coordinate of center
    cX = int(M["m10"] / (M["m00"] + 1e-5))
    cY = int(M["m01"] / (M["m00"] + 1e-5))


    
    if (cX is not 0 and cY is not 0):
        # put text and highlight the center
        cv2.circle(image, (cX, cY), 17, (0, 128, 128), -1)

    return image