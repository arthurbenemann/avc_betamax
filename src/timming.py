 
import time
from math import log10
 
class Timming:

    start_time = time.time()
    sum = 0
    skip = False;
    
    def __init__(self, shouldPrint):
        self.skip = not shouldPrint
    
    
    
    def tic(self,msg):
        if self.skip:
            return
        now = time.time()
        print(msg.ljust(20) +'\t' + eng_str(now-self.start_time))
        self.sum += now-self.start_time
        self.start_time = now
        return
    
    def sumAndReset(self):
        if self.skip:
            return
        print(("Sum").ljust(20) +'\t' + eng_str(self.sum))
        self.sum = 0
        print("------------------------------")
        return
    
    
        
def eng_str(x):
    y = abs(x)
    if y == 0:
        return '0'
    exponent = int(log10(y))
    engr_exponent = exponent - exponent%3
    z = y/10**engr_exponent
    sign = '-' if x < 0 else ''
    return sign+str(z)+'e'+str(engr_exponent)
        