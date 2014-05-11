import cv2
import circleDetection
from colorSelector import ColorSelector
from camera import Camera
from plot import Plot
from kalman import Kalman
from particleFilter import ParticleFilter
from timming import Timming

colorSel = ColorSelector()
camera = Camera()
plot = Plot()
kalman = Kalman()
particleFilter = ParticleFilter()
timer = Timming(False)

def main():
    colorSel.createTrackBars()
    while True:    
        loop()        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break        
    camera.release()
    cv2.destroyAllWindows()
    

def loop():
    timer.tic("start")
    frame = camera.getFrame()
    timer.tic("frame")
    
    # Image Processing    
    colour_low, colour_high = colorSel.getColorFilter()
    timer.tic("color Filter")
                
    circles = circleDetection.detectBallonInFrame(frame, colour_low, colour_high)
    timer.tic("detect ballon")
        
    circleDetection.drawCirclesInFrame(circles, frame)
    timer.tic("draw circles")
    
    if not (circles is None):
        z = camera.transformCameraToWorld(circles[0, 0, :])
    else:
        z = None
    timer.tic("transform to world")
        
        
    #Kalman
    kalman.predict()            
    if not (z is None):
        kalman.update(z)
    else:
        kalman.updateWithoutMeasurament()
    timer.tic("kalman")
        
    #Particle Filter
    if not (z is None):
        particleFilter.update(z)
    else:
        particleFilter.updateWithoutMeasurament()
    timer.tic("particle filter")
    
    #Graphics
    cv2.imshow('result', frame)
    '''       
    if not (circles is None):        
        plot.newData(z, kalman.x, kalman.P)
        plot.newParticleFilterData(z,particleFilter)
    else:
        plot.newData(None, kalman.x, kalman.P)
        plot.newParticleFilterData(None,particleFilter)    
    '''    
    timer.tic("Graphics")
    
    timer.sumAndReset()

if __name__ == "__main__":
    main()
