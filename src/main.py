import cv2
import circleDetection
from colorSelector import ColorSelector
from camera import Camera


# define image resolution
img_width = 640
img_height = 480

colorSel = ColorSelector()
camera = Camera()

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
        
    colour_low, colour_high = colorSel.getColorFilter()
                
    circles = circleDetection.detectBallonInFrame(frame, colour_low, colour_high)
        
    circleDetection.drawCirclesInFrame(circles, frame)
    cv2.imshow('result', frame)
        
    if not (circles is None):
        z = camera.transformCameraToWorld(circles[0,0,0],circles[0,0,1],circles[0,0,2])
        print(z)

if __name__ == "__main__":
    main()