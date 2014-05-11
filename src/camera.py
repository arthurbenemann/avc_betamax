import cv2
import math

class Camera:
    video_capture = cv2.VideoCapture(0)

    def transformCameraToWorld(self, xPixel,yPixel,size):
        # Calculate measurament variables
        u = (xPixel / 320.0) - 1
        v = (yPixel / 240.0) - 1
        pho = 20.0 / size        
        z = [pho * 1.0 / math.sqrt(1 + u * u), pho * u / math.sqrt(1 + u * u)]
        return z
    
    def getFrame(self):
        _, frame = self.video_capture.read()
        return frame

    
    def release(self):
        self.video_capture.release()
    
    


    

