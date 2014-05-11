import numpy

PARTICLE_NUMBER = 50

class ParticleFilter():
    pos = numpy.random.random_sample((PARTICLE_NUMBER,3))
    weights = numpy.ones(PARTICLE_NUMBER)/PARTICLE_NUMBER 
    
    def addNoise(self):
        for i in self.pos:
            i[0] = i[0]+ numpy.random.randn()*0.01
            i[1] = i[1]+ numpy.random.randn()*0.01
            i[2] = i[2]+ numpy.random.randn()*0.01 
    
    def update(self,z):
        self.addNoise()
        self.reweight(z)

    def reweight(self, z):
        for i in range(PARTICLE_NUMBER):
            self.weights[i] = (numpy.hypot(z[0]-self.pos[i,0], z[1]-self.pos[i,1]))
        self.weights = self.weights/self.weights.max()
    
    def updateWithoutMeasurament(self):
        self.addNoise()
    
    
    
    
    