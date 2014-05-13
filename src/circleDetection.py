import cv2
import numpy
from timming import timeit

@timeit
def detectBallonInFrame(frame, colour_low, colour_high):
    # small = cv2.pyrDown(frame)
    
    # Process image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Threshold the HSV image
    mask = cv2.inRange(hsv, colour_low, colour_high)
#   cv2.imshow('threshold', mask)

    # Erode
    erode_kernel = numpy.ones((5, 5), numpy.uint8)
    eroded_img = cv2.erode(mask, erode_kernel, iterations=1)
    
    # dilate
    dilate_kernel = numpy.ones((20, 20), numpy.uint8)
    dilate_img = cv2.dilate(eroded_img, dilate_kernel, iterations=1)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=dilate_img)
    
    # Transform to Gray scale
    img = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('mask',res)

    # Blur and Hough
    img = cv2.medianBlur(img, 5)
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 2, 200, numpy.array([]), 100, 30, 1, 200)
    return circles


def drawCirclesInFrame(circles, frame):
    # check if any circles were found
    if not (circles is None):
        circles = numpy.uint16(numpy.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            break  # Draw just the first circle
    return frame


def getWorldCoordForFirstCircle(circles, camera):
    if not (circles is None):
        z = camera.transformNormalizedCamera(circles[0, 0, :])
        print("Measurament:\t%+0.3f\t%+0.3f\t%+0.3f" %(z[0],z[1],z[2]))
    else:
        z = None
    return z

