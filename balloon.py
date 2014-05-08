#!/usr/bin/env python

# built-in modules
import sys
from time import clock

import numpy as np
import cv2
import cv2.cv as cv

# local modules
import video
import math
import matplotlib.pyplot as plt

if __name__ == '__main__':

    try:
        fn = sys.argv[1]
    except:
        fn = 0
    cam = video.create_capture(fn, fallback='synth:bg=../cpp/baboon.jpg:class=chess:noise=0.05')


    # default colour filters (this is for a yellow tennis ball)
    h_low = 0
    h_high = 10
    s_low = 120
    s_high = 250
    v_low = 170
    v_high = 255

    # call back for trackbar movements
    def empty_callback(x):
	pass

    # create trackbars for color change
    cv2.namedWindow('Colour Filters')
    cv2.createTrackbar('Hue min','Colour Filters',h_low,255,empty_callback)
    cv2.createTrackbar('Hue max','Colour Filters',h_high,255,empty_callback)
    cv2.createTrackbar('Sat min','Colour Filters',s_low,255,empty_callback)
    cv2.createTrackbar('Sat max','Colour Filters',s_high,255,empty_callback)
    cv2.createTrackbar('Bgt min','Colour Filters',v_low,255,empty_callback)
    cv2.createTrackbar('Bgt max','Colour Filters',v_high,255,empty_callback)



    #Capture a single frame just to show the result window first
    flag, frame = cam.read()
    cv2.imshow('result',frame);

    #Display the plot
    fig=plt.figure()
    plt.show(block=False)
    plt.hold(False)

	

    while True:
	# Read frame
        flag, frame = cam.read()
        cv2.imshow('camera', frame)
        small = cv2.pyrDown(frame)
	small = frame

	#Process image
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)


	# get latest trackbar positions
	h_low = cv2.getTrackbarPos('Hue min','Colour Filters')
	h_high = cv2.getTrackbarPos('Hue max','Colour Filters')
	s_low = cv2.getTrackbarPos('Sat min','Colour Filters')
	s_high = cv2.getTrackbarPos('Sat max','Colour Filters')
	v_low = cv2.getTrackbarPos('Bgt min','Colour Filters')
	v_high = cv2.getTrackbarPos('Bgt max','Colour Filters')

        # use trackbar positions to filter image
        colour_low = np.array([h_low,s_low,v_low])
        colour_high = np.array([h_high,s_high,v_high])

        # Threshold the HSV image
        mask = cv2.inRange(hsv, colour_low, colour_high)
	cv2.imshow('threshold',mask)

        # Erode
        erode_kernel = np.ones((5,5),np.uint8);
        eroded_img = cv2.erode(mask,erode_kernel,iterations = 1)

        # dilate
        dilate_kernel = np.ones((20,20),np.uint8);
        dilate_img = cv2.dilate(eroded_img,dilate_kernel,iterations = 1)

 	# Bitwise-AND mask and original image
        res = cv2.bitwise_and(small,small, mask = dilate_img)

	#Transform to Gray scale
        img = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

	cv2.imshow('mask',res)

	#Blur and Hough
	img = cv2.medianBlur(img, 5)

	circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 2, 200, np.array([]), 100, 30, 1, 200)


        # draw circles around the circles
	cimg = small.copy() # numpy function
	  # check if any circles were found
        if not (circles is None):
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

		print('x:'+str(i[0]).rjust(3),'y:'+str(i[1]).rjust(3),'size:'+str(i[2]).rjust(3),'-'*i[2])

		#Calculate measurament variables
		u= (i[0]/320.0)-1
		pho = 20.0/i[2]

		
		x_ = pho*1.0/math.sqrt(1+u*u)
		y_ = pho*u/math.sqrt(1+u*u)


		print(x_,y_)
		plt.plot(x_, y_, 'ro')

           	plt.axis([0,2,-1,1])
		plt.draw()

		break
	else:
		print('-')
	cv2.imshow('result',cimg)


	


	# Finish program
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    cv2.destroyAllWindows()
