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






def main():




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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    video_capture.release()
    

  

if __name__ == "__main__":
    main()
