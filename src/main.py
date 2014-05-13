import cv2
import circleDetection
from colorSelector import ColorSelector
from camera import Camera
from plot import Plot
from particleFilter import ParticleFilter
from timming import timeit

colorSel = ColorSelector()
camera = Camera()
plot = Plot()
particleFilter = ParticleFilter()

def main():
    colorSel.createTrackBars()
    while True:    
        loop()        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break        
    camera.release()
    cv2.destroyAllWindows()
    
@timeit
def loop():
    frame = camera.getFrame()
    
    # Image Processing    
    colour_low, colour_high = colorSel.getColorFilter()
    circles = circleDetection.detectBallonInFrame(frame, colour_low, colour_high)
    z = circleDetection.getWorldCoordForFirstCircle(circles, camera)        
        
    # Filters    
    particleFilter.update(z)
    
    # Graphics
    circleDetection.drawCirclesInFrame(circles, frame)
    # frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25) 
    cv2.imshow('result', frame)
                  
    plot.newParticleFilterData(None, particleFilter, True)

if __name__ == "__main__":
    main()
