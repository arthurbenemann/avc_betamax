import numpy

SYSTEM_NOISE = 0.02
MEASURAMENT_NOISE = 0.01
PARTICLE_NUMBER = 1000

class ParticleFilter():
    pos = numpy.random.random_sample((PARTICLE_NUMBER,3))
    weights = numpy.ones(PARTICLE_NUMBER)/PARTICLE_NUMBER 
    
    def addNoise(self):
        for i in self.pos:
            i[0] = i[0]+ numpy.random.randn()*SYSTEM_NOISE
            i[1] = i[1]+ numpy.random.randn()*SYSTEM_NOISE
            i[2] = i[2]+ numpy.random.randn()*SYSTEM_NOISE 
    
    def update(self,z):
        self.addNoise()
        self.reweight(z)
        self.resample()

    def reweight(self, z):
        for i in range(PARTICLE_NUMBER):
            temp = numpy.hypot(z[0]-self.pos[i,0], z[1]-self.pos[i,1])
            self.weights[i] =(1/numpy.sqrt(2*numpy.pi*MEASURAMENT_NOISE)) * numpy.exp(-numpy.power(temp,2)/(2*MEASURAMENT_NOISE))
             
        self.weights = self.weights/self.weights.sum()
    
    def resample(self):
        cumsum = numpy.cumsum(self.weights)
        posCopy = numpy.copy(self.pos)
        for i in range(PARTICLE_NUMBER):
            rand = numpy.random.rand()
            sample = numpy.where(cumsum>=rand)[0][0] #TODO find faster function
            self.pos[i,:] = posCopy[sample,:] 
            
    def mean(self):
        return numpy.mean(self.pos, axis=0)
    
    def updateWithoutMeasurament(self):
        self.addNoise()
    
    
    
    
    