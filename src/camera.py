import cv2
import numpy
import time

# define image resolution
img_width = 1280
img_height = 720
focal = 0.05

#Ball parameters
realSize = 1000

class Camera:
    video_capture = cv2.VideoCapture(-1)
    
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, img_width)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, img_height)
    print(str(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))+"x"+str(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    
    start_time = time.time()
    fps = 0

    def transformNormalizedCamera(self, circle):
        xPixel = circle[0]
        yPixel = circle[1]
        apparentSize = circle[2]
        
        # Calculate measurament variables
        u = 2 * (xPixel / img_width) - 1
        v = -(2 * (yPixel / img_height) - 1)        
        return numpy.array([u,v,apparentSize])
    
    def getFrame(self):
        _, frame = self.video_capture.read()
        
        self.fps += 1
 
        if self.fps % 10 == 0:
            currtime = time.time()
            numsecs = currtime - self.start_time
            self.start_time = currtime
            self.fps = self.fps / numsecs
            print "average FPS:", self.fps
            self.fps = 0;
            
        return frame

    
    def release(self):
        self.video_capture.release()