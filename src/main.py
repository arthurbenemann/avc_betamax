import cv2
import circleDetection
from colorSelector import ColorSelector
from camera import Camera
from plot import Plot
from kalman import Kalman
from particleFilter import ParticleFilter

colorSel = ColorSelector()
camera = Camera()
plot = Plot()
kalman = Kalman()
particleFilter = ParticleFilter()

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
    
    z = circleDetection.getWorldCoordForFirstCircle(circles,camera)        
        
    #Filters    
    kalman.update(z)
    particleFilter.update(z)
    
    #Graphics
    circleDetection.drawCirclesInFrame(circles, frame)
    cv2.imshow('result', frame)
                  
    plot.newData(z, kalman)
    plot.newParticleFilterData(z,particleFilter)    
    

if __name__ == "__main__":
    main()
