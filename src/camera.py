import cv2
import math
import time
import numpy

# define image resolution
img_width = 1280
img_height = 1024
focal = 1

#Ball parameters
realSize = 10


class Camera:
    video_capture = cv2.VideoCapture(-1)
    
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, img_width)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, img_height)
    print(str(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))+"x"+str(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    
    start_time = time.time()
    fps = 0

    def transformCameraToWorld(self, circle):
        xPixel = circle[0]
        yPixel = circle[1]
        apparentSize = circle[2]
        
        # Calculate measurament variables
        u = 2 * (xPixel / img_width) - 1
        v = -(2 * (yPixel / img_height) - 1)
        pho = (realSize / apparentSize) * focal        
        z = numpy.array([pho * math.sin(math.atan(u/focal)), pho * math.sin(math.atan(v/focal)), pho * math.cos(math.atan((v)/focal))])  # this is wrong, the correct measurament equation should be added
        return z
    
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
    
    


    

