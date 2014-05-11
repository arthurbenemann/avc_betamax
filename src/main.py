import cv2
import circleDetection
from colorSelector import ColorSelector
from camera import Camera
from plot import Plot
from kalman import Kalman


# define image resolution
img_width = 640
img_height = 480

colorSel = ColorSelector()
camera = Camera()
plot = Plot()
kalman = Kalman()

def main():
    colorSel.createTrackBars()
    while True:    
        loop()        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break        
    camera.release()
    cv2.destroyAllWindows()
    

def loop():
    frame = camera.getFrame()
    
    # Image Processing    
    colour_low, colour_high = colorSel.getColorFilter()
                
    circles = circleDetection.detectBallonInFrame(frame, colour_low, colour_high)
        
    circleDetection.drawCirclesInFrame(circles, frame)
    
    #Kalman
    kalman.predict()
            
    if not (circles is None):
        z = camera.transformCameraToWorld(circles[0, 0, :])
        kalman.update(z)
    else:
        kalman.updateWithoutMeasurament()
    
    #Graphics
    cv2.imshow('result', frame)
        
    if not (circles is None):        
        plot.newData(z, kalman.x, kalman.P)
    else:
        plot.newData(None, kalman.x, kalman.P)

if __name__ == "__main__":
    main()
