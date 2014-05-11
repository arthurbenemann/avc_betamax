import cv2
import numpy

# call back for trackbar movements
def empty_callback(self):
        pass

class ColorSelector:
    # default Color filters (this is for a yellow tennis ball)
    h_low = 0
    h_high = 10
    s_low = 120
    s_high = 255
    v_low = 115
    v_high = 255

    def getColorFilter(self):
        # get latest trackbar positions
        self.h_low = cv2.getTrackbarPos('Hue min', 'Color Filters')
        self.h_high = cv2.getTrackbarPos('Hue max', 'Color Filters')
        self.s_low = cv2.getTrackbarPos('Sat min', 'Color Filters')
        self.s_high = cv2.getTrackbarPos('Sat max', 'Color Filters')
        self.v_low = cv2.getTrackbarPos('Val min', 'Color Filters')
        self.v_high = cv2.getTrackbarPos('Val max', 'Color Filters')

        color_low = numpy.array([self.h_low, self.s_low, self.v_low])
        color_high = numpy.array([self.h_high, self.s_high, self.v_high])
        return color_low, color_high

    def createTrackBars(self):
        cv2.namedWindow('Color Filters')
        cv2.createTrackbar('Hue min', 'Color Filters', self.h_low, 255, empty_callback)
        cv2.createTrackbar('Hue max', 'Color Filters', self.h_high, 255, empty_callback)
        cv2.createTrackbar('Sat min', 'Color Filters', self.s_low, 255, empty_callback)
        cv2.createTrackbar('Sat max', 'Color Filters', self.s_high, 255, empty_callback)
        cv2.createTrackbar('Val min', 'Color Filters', self.v_low, 255, empty_callback)
        cv2.createTrackbar('Val max', 'Color Filters', self.v_high, 255, empty_callback)    
