import numpy
from timming import timeit
import scipy.stats
import camera
import math

SYSTEM_NOISE = 0.05
MEASURAMENT_NOISE = 0.1
PARTICLE_NUMBER = 100

def findFirst(cumsum, rand):
    for i in range(PARTICLE_NUMBER):
        if cumsum[i] >= rand:
            return i
    return None

class ParticleFilter():
    pos = numpy.random.random_sample((PARTICLE_NUMBER, 3))
    weights = numpy.ones(PARTICLE_NUMBER) / PARTICLE_NUMBER  
    mesuramentPDF = scipy.stats.norm(0, MEASURAMENT_NOISE)
    projected = numpy.zeros((PARTICLE_NUMBER, 3)) # dumy init
    
    @timeit
    def update(self, z):
        self.addNoise()
        if not z is None:
            self.reweight(z)
            self.resample(z)

    @timeit
    def addNoise(self):
        for i in self.pos:
            i[0] = i[0] + numpy.random.randn() * SYSTEM_NOISE
            i[1] = i[1] + numpy.random.randn() * SYSTEM_NOISE
            i[2] = i[2] + numpy.random.randn() * SYSTEM_NOISE 

    @timeit
    def reweight(self, measurament):
        for i in range(PARTICLE_NUMBER):
            x = self.pos[i,0]
            y = self.pos[i,1]
            z = self.pos[i,2]
            self.projected[i,:] = camera.focal*numpy.array([x/z,y/z,camera.realSize/math.sqrt(x*x+y*y+z*z)])   
        
        temp = numpy.apply_along_axis(numpy.linalg.norm, 1, measurament - self.projected)  # norm of the difference for all particles
        self.weights = self.mesuramentPDF.pdf(temp)
             
        weightsSum = self.weights.sum()
        if weightsSum > 0:
            self.weights = self.weights / weightsSum
    
    @timeit
    def resample(self, z):
        cumsum = numpy.cumsum(self.weights)
        posCopy = numpy.copy(self.pos)
        for i in range(PARTICLE_NUMBER):
            rand = numpy.random.rand()
            sample = findFirst(cumsum, rand)
            if sample is None:
                self.pos[i, :] = numpy.random.random_sample((1, 3))  # if sample has zero probability create sample at random location
            else:
                self.pos[i, :] = posCopy[sample, :] 
    @timeit            
    def mean(self):
        return numpy.mean(self.pos, axis=0)
    
    
    
