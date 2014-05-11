import numpy

SYSTEM_NOISE = 0.01
PARTICLE_NUMBER = 100

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
            self.weights[i] = numpy.exp(-1*numpy.hypot(z[0]-self.pos[i,0], z[1]-self.pos[i,1]))
        self.weights = self.weights/self.weights.sum()
    
    def resample(self):
        cumsum = numpy.cumsum(self.weights)
        posCopy = numpy.copy(self.pos)
        for i in range(PARTICLE_NUMBER):
            rand = numpy.random.rand()
            sample = numpy.where(cumsum>rand)[0][0]
            self.pos[i,:] = posCopy[sample,:] 
            
    def mean(self):
        return numpy.mean(self.pos, axis=0)
    
    def updateWithoutMeasurament(self):
        self.addNoise()
    
    
    
    
    