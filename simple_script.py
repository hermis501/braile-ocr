# simple script found in stackoverflow
import cv2
import numpy as np
photo="e:/braille/braille_scan.jpg"
img      = cv2.imread(photo)
gray     = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur     = cv2.GaussianBlur(gray,(3,3),0)
thres    = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,4)
blur2    = cv2.medianBlur(thres,3)
ret2, th2 = cv2.threshold(blur2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
blur3    = cv2.GaussianBlur(th2,(3,3),0)
ret3,th3 = cv2.threshold(blur3,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Find connected components and extract the mean height and width
output = cv2.connectedComponentsWithStats(255-th3, 6, cv2.CV_8U)
mean_h = np.mean(output[2][:,cv2.CC_STAT_HEIGHT])
mean_w = np.mean(output[2][:,cv2.CC_STAT_WIDTH])

# Find empty rows, defined as having less than mean_h/2 pixels
empty_rows = []
for i in range(th3.shape[0]):
	if np.sum(255-th3[i,:]) < mean_h/2.0:
		empty_rows.append(i)           

# Group rows by labels
d = np.ediff1d(empty_rows, to_begin=1)

good_rows   = []
good_labels = []
label       = 0
# 1: assign labels to each row
# based on whether they are following each other or not (i.e. diff >1)
for i in range(1,len(empty_rows)-1):
	if d[i+1] == 1:
		good_labels.append(label)
		good_rows.append(empty_rows[i])
	elif d[i] > 1 and d[i+1] > 1:
		label = good_labels[len(good_labels)-1] + 1

# 2: find the mean row value associated with each label, and color that line in green in the original image
for i in range(label):
	frow = np.mean(np.asarray(good_rows)[np.where(np.asarray(good_labels) == i)])
	img[int(frow),:,1] = 255 

# Display the image with the green rows
cv2.imshow('test',img)
cv2.waitKey(0)
