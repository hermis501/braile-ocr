import math
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.color import label2rgb
import cv2
import sys,os

def get_input():	
	path = sys.argv[1]
	if os.path.exists(path):
		return cv2.imread(path,0)		#Here 0 Means Loading the image as Grey Scale
	else:
		print("error")


def distance(x1,y1,x2,y2):
	return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
	
def Get_Letter(value):
	if value == 0:
		return " "
	elif value==32:
		return "a"
	elif value==48:
		return "b"
	elif value==36:
		return "c"
	elif value==38:
		return "d"
	elif value==34:
		return "e"
	elif value==52:
		return "f"
	elif value==54:
		return "g"
	elif value==50:
		return "h"
	elif value==20:
		return "i"
	elif value==22:
		return "j"
	elif value==40:
		return "k"
	elif value==56:
		return "l"
	elif value==44:
		return "m"
	elif value==46:
		return "n"
	elif value==42:
		return "o"
	elif value==60:
		return "p"
	elif value==62:
		return "q"
	elif value==58:
		return "r"
	elif value==28:
		return "s"
	elif value==30:
		return "t"
	elif value==41:
		return "u"
	elif value==57:
		return "v"
	elif value==23:
		return "w"
	elif value==45:
		return "x"
	elif value==47:
		return "y"
	elif value==43:
		return "z"
	elif value==15:
		return "#"
	elif value==9:
		return "-"
	return " "
	

def Get_Text():
	dot_dist = (final_radius/0.8)*2.5

	ans = ""

	for j in range(len(y_list)):
		for i in range(len(x_list)):
			#print(j,i)
			char = 0
			for k in range(2):
				for h in range(3):
					x_pos = x_list[i] + dot_dist*k
					
					y_pos = y_list[j] + dot_dist*h
					x_pos = int(round(x_pos))
					y_pos = int(round(y_pos))
					if x_pos>=image.shape[1] or y_pos>=image.shape[0]:
						break
					if label_img[y_pos][x_pos]!=0:
						char = char*2 + 1
			#			print(k,h,"a'''")
					else:
						char = char*2
			ans += Get_Letter(char)
		ans+="\n"



	final_ans = ""
	i = 0
	while i < len(ans) :
		if ans[i] =='#':
			i = i+1
			while ans[i] !=" " and ans[i] != "\n":
				temp = ord(ans[i])-96
				if temp ==10:
					temp = 0
				i = i+1
				final_ans += str(temp)
			final_ans +=" "
				
		else:
			final_ans+=ans[i]
		i = i+1	


	print("Text:")
	print("******************")
	print(final_ans,end = "")
	print("******************")
#End of Get_Text Function

def Threshold(image):
	val,image = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)			#OTSU'S

	image = 255-image
	
	return image

def stat_regions(regions):

	areas = []
	for region in regions:

		if region.label!=1:

			areas.append(region.area)
	
	areas = np.array(areas)	
	mean_area = np.mean(areas)
	std_area = np.std(areas)
	
	return mean_area,std_area


def Dots_Stats(regions,mean_area,std_area):
	x_low = math.inf
	x_high = 0.0
	y_low = math.inf
	y_high = 0.0



	radii = np.array([])
	detected_circles_x = np.array([])
	detected_circles_y = np.array([])

	for region in regions:
		
		if abs(region.area-mean_area)<=5*std_area:				#Very Big and Very Small Dots will be removed
		
			radius = region.equivalent_diameter/2
			radii = np.append(radii,radius)
			
			radius = round(radius)

			
			center_x,center_y = region.centroid				#centroid gives row,column
					

			detected_circles_x = np.append(detected_circles_x,center_y)		
			detected_circles_y = np.append(detected_circles_y,center_x)


			x_low = min(x_low,center_y)
			x_high = max(x_high,center_y)

			
			y_low = min(y_low,center_x)
			y_high = max(y_high,center_x)
			

			center_x = int(round(center_x))
			center_y = int(round(center_y))

			cv2.circle(circle_img,(center_y,center_x),radius,(0,255,0))

		
	final_radius = np.mean(radii)
	std_dev = np.std(radii)
	print(final_radius,std_dev)
	return x_low,x_high,y_low,y_high,final_radius,std_dev
	



#Main Program Begins here


image = get_input()

image = Threshold(image)


label_img = label(image)
regions = regionprops(label_img)

print("No of Dots Detected : ",len(regions))


circle_img = image
#circle_img = np.zeros((image.shape[0],image.shape[1]))
circle_img = 255-circle_img


mean_area,std_area = stat_regions(regions)

x_low,x_high,y_low,y_high,final_radius,std_dev = Dots_Stats(regions,mean_area,std_area)


print("Radius of Dot : ",final_radius,"Std_dev: ",std_dev)



x_list = []
x_list.append(x_low)

while x_low<x_high:
	x_low = x_low + (final_radius/0.8)*6
	if x_low<image.shape[1]:
		x_list.append(x_low)


y_list = []
y_list.append(y_low)

while y_low<y_high:
	y_low = y_low + (final_radius/0.8)*10
	if y_low<image.shape[0]:
		y_list.append(y_low)

x_list = np.array(x_list)
y_list = np.array(y_list)



for i in range(len(x_list)):
	for j in range(image.shape[0]):
	
		x_coord = int(round(x_list[i]))
		
		if x_coord >= image.shape[1]:
			break; 
		
		if label_img[j][x_coord]!=0:
			
			current_region = regions[label_img[j][x_coord]-1]
			
			if ((current_region.equivalent_diameter/2) -final_radius) <=5*std_dev:
				
				x_list[i] = current_region.centroid[1]
				
				if i<len(x_list)-1:
					
					x_list[i+1] = x_list[i] + ((final_radius/0.8)*6)
					
					break




for i in range(len(y_list)):

	y_coord = int(round(y_list[i]))
	
	if y_coord >= image.shape[0]:
		break; 

	
	for j in range(image.shape[1]):

		if label_img[y_coord][j]!=0:

			current_region = regions[label_img[y_coord][j]-1]

			if abs((current_region.equivalent_diameter/2) -final_radius) <=5*std_dev:

				y_list[i] = current_region.centroid[0]

				if i<len(y_list)-1:

					y_list[i+1] = y_list[i] + (final_radius/0.8)*10

					break
			
			

print(x_list)
print("a")
print(y_list)
Get_Text()


for i in range(len(x_list)):
	cv2.line(circle_img,(int(round(x_list[i])),0),(int(round(x_list[i])),circle_img.shape[0]),(0,255,0))


for j in range(len(y_list)):
	cv2.line(circle_img,(0,int(round(y_list[j]))),(circle_img.shape[1],int(round(y_list[j]))),(0,255,0))

cv2.imwrite('detected circles.jpg',circle_img)

