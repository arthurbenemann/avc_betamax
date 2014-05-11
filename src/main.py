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
        
    circleDetection.drawCirclesInFrame(circles, frame)
    
    #Kalman
    kalman.predict()
            
    if not (circles is None):
        z = camera.transformCameraToWorld(circles[0, 0, :])
        kalman.update(z)
        particleFilter.update(z)
    else:
        kalman.updateWithoutMeasurament()
        particleFilter.updateWithoutMeasurament()
    
    #Graphics
    cv2.imshow('result', frame)
       
    if not (circles is None):        
        plot.newData(z, kalman.x, kalman.P)
        plot.newParticleFilterData(z,particleFilter)
    else:
        plot.newData(None, kalman.x, kalman.P)
        plot.newParticleFilterData(None,particleFilter)    

if __name__ == "__main__":
    main()
