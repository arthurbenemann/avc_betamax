#!/usr/bin/env python

# built-in modules
import sys
from time import clock

import numpy as np
import cv2
import cv2.cv as cv

# local modules
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


# define image resolution
img_width = 640
img_height = 480

def get_camera():
    # setup video capture
    video_capture = cv2.VideoCapture(0-1)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, img_width)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, img_height)

    # check we can connect to camera
    if not video_capture.isOpened():
        print "failed to open camera, exiting!"
        sys.exit(0)

    return video_capture


# call back for trackbar movements
def empty_callback(x):
    pass

def main():
        
    video_capture = get_camera()


    # default colour filters (this is for a yellow tennis ball)
    h_low = 0
    h_high = 10
    s_low = 120
    s_high = 250
    v_low = 130
    v_high = 255

    # create trackbars for color change
    cv2.namedWindow('Colour Filters')
    cv2.createTrackbar('Hue min', 'Colour Filters', h_low, 255, empty_callback)
    cv2.createTrackbar('Hue max', 'Colour Filters', h_high, 255, empty_callback)
    cv2.createTrackbar('Sat min', 'Colour Filters', s_low, 255, empty_callback)
    cv2.createTrackbar('Sat max', 'Colour Filters', s_high, 255, empty_callback)
    cv2.createTrackbar('Bgt min', 'Colour Filters', v_low, 255, empty_callback)
    cv2.createTrackbar('Bgt max', 'Colour Filters', v_high, 255, empty_callback)


    # Display the plot
    fig = plt.figure()
    plt.show(block=False)
    plt.hold(False)

	
    # Init Kalman

    A = np.array([[1, 0], [0, 1]])  # Process model
    H = np.array([[1, 0], [0, 1]])  # Measurament model
    Q = np.eye(2) * 0.002  # Process covariance
    R = np.array([[5, 0], [0, 1]])  # Measurament covariance
    x = np.array([0, 0])  # Initial pos
    P = np.eye(2) * 100000000  # Initial Covariance
    z = np.array([0, 0])  # Dummy init

    while True:
        # Read frame
        _, frame = video_capture.read()
        cv2.imshow('camera', frame)
        
        continue

        # get latest trackbar positions
        h_low = cv2.getTrackbarPos('Hue min', 'Colour Filters')
        h_high = cv2.getTrackbarPos('Hue max', 'Colour Filters')
        s_low = cv2.getTrackbarPos('Sat min', 'Colour Filters')
        s_high = cv2.getTrackbarPos('Sat max', 'Colour Filters')
        v_low = cv2.getTrackbarPos('Bgt min', 'Colour Filters')
        v_high = cv2.getTrackbarPos('Bgt max', 'Colour Filters')

        # use trackbar positions to filter image
        colour_low = np.array([h_low, s_low, v_low])
        colour_high = np.array([h_high, s_high, v_high])


        circles = detectBallonInFrame(frame, colour_low, colour_high)

        cimg = drawCirclesInFrame(circles,frame)

        if not (circles is None):
            z = transformCameraToWorld(circles[0,0,0],circles[0,0,1],circles[0,0,2])
        
        # Kalman Predict
        xp = A.dot(x)
        Pp = A.dot(P.dot(A.T)) + Q
        
        if not (circles is None):
    		# Kalman Update
    		K = Pp.dot(H.T.dot(np.linalg.inv(H.dot(Pp.dot(H.T)) + R)))		
    		x = xp + K.dot(z - H.dot(xp))
    		P = Pp - K.dot(H.dot(Pp))			
        else:
            P = Pp

	
    	# Plot
    	if not (circles is None):
    		plt.plot(z[0], z[1], 'ro', x[0], x[1], 'bo')
    	else:
    		plt.plot(x[0], x[1], 'bo')
          	plt.axis([0, 2, -1, 1])
    	
    	if (P.max() <= 1):
    		plt.gca().add_patch(Ellipse(xy=(x[0], x[1]), width=P[0, 0], height=P[1, 1],
                            edgecolor='b', fc='None', lw=2))
    	#plt.draw()
    	print(P)
    	print(P.max() <= 1)
    	print(x)
    
    	#cv2.imshow('result', cimg)
	
    	# Finish program
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
        cv2.destroyAllWindows()
    
def transformCameraToWorld(xPixel,yPixel,size):
    # Calculate measurament variables
    u = (xPixel / 320.0) - 1
    v = (yPixel / 240.0) - 1
    pho = 20.0 / size        
    z = [pho * 1.0 / math.sqrt(1 + u * u), pho * u / math.sqrt(1 + u * u)]
    return z
    
def drawCirclesInFrame(circles, frame):
    # check if any circles were found
    if not (circles is None):
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            break # Draw just the first circle
    return frame
            

def detectBallonInFrame(frame, colour_low, colour_high):
    #small = cv2.pyrDown(frame)
    
    # Process image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Threshold the HSV image
    mask = cv2.inRange(hsv, colour_low, colour_high)
#   cv2.imshow('threshold', mask)

    # Erode
    erode_kernel = np.ones((5, 5), np.uint8)
    eroded_img = cv2.erode(mask, erode_kernel, iterations=1)
    
    # dilate
    dilate_kernel = np.ones((20, 20), np.uint8)
    dilate_img = cv2.dilate(eroded_img, dilate_kernel, iterations=1)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=dilate_img)
    
    # Transform to Gray scale
    img = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
# 	cv2.imshow('mask',res)

    # Blur and Hough
    img = cv2.medianBlur(img, 5)
    circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 2, 200, np.array([]), 100, 30, 1, 200)
    return circles


if __name__ == "__main__":
    main()
