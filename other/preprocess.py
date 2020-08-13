import numpy as np
import cv2
from matplotlib import pyplot as plt

import sys,os

def get_input():	
	path = sys.argv[1]
	if os.path.exists(path):
		return cv2.imread(path)		#Here 0 Means Loading the image as Grey Scale
	else:
		print("error")




img = get_input()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#Thresh makes dots and text white, the rest black


cv2.imwrite("small.png",thresh)


kernel = np.ones((3,3),np.uint8)

opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 3)
#Erosion Makes the object in White thinner


dilated = cv2.dilate(opening,kernel,iterations=2)
#Dilating Makes the object in White Thicker


image = cv2.bitwise_and(thresh,dilated)
image = 255- image



#new = np.copy(img)
color = (255,255,255)


new = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)


img[np.where((new == [255,255,255]).all(axis = 2))] = color 


cv2.imwrite("small_removed.png",img)
