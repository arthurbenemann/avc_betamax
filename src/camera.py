import cv2
import math

# define image resolution
img_width = 640
img_height = 480


class Camera:
    video_capture = cv2.VideoCapture(0)

    def transformCameraToWorld(self, circle):
        xPixel = circle[0]
        yPixel = circle[1]
        size = circle[2]
        
        # Calculate measurament variables
        u = 2*(xPixel / img_width) - 1
        v = 2*(yPixel / img_height) - 1
        pho = 20.0 / size        
        z = [pho * 1.0 / math.sqrt(1 + u * u), pho * u / math.sqrt(1 + u * u)]
        return z
    
    def getFrame(self):
        _, frame = self.video_capture.read()
        return frame

    
    def release(self):
        self.video_capture.release()
    
    


    

