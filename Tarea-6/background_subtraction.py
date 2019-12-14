import cv2
import numpy as np
import imutils


def background_subtraction(
        img,
        background,
        sm,
        threshold=150,
        bar1=80,
        bar2=50,
        radio=15,
        showProcess=False):

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

    # calculate x,y coordinate of center
    cX = int(M["m10"] / (M["m00"] + 1e-5))
    cY = int(M["m01"] / (M["m00"] + 1e-5))

    if(len(cnts)!=0):
        c = max(cnts, key = cv2.contourArea)
    
        cv2.drawContours(contours_image, [c], -1, (0, 255, 0), 2)
        if (cX is not 0 and cY is not 0):
	        # put text and highlight the center
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
