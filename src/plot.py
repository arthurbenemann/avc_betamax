from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt


class Plot:
    def newData(self, z, kalman):        
        plt.figure("Kalman")
        plt.clf()
        plt.hold(True)
        plt.plot(kalman.x[0], kalman.x[1], 'bo')
        if (z is not None):
            plt.plot(z[0], z[1], 'ro', kalman.x[0], kalman.x[1], 'bo')
        
        if (kalman.P.max() <= 1):
            plt.gca().add_patch(Ellipse(xy=(kalman.x[0], kalman.x[1]), width=kalman.P[0, 0], height=kalman.P[1, 1], edgecolor='b', fc='None', lw=2))
            
        plt.axis([0, 2, -1, 1])            
        plt.draw()
        plt.show(block=False)

    
    def newParticleFilterData(self, z, particleFilter):
        plt.figure("particleFilter");
        plt.clf()
        plt.hold(True)
        estimate = particleFilter.mean()
        plt.plot(estimate[0], estimate[1], 'bo')
        plt.scatter(particleFilter.pos[:, 0], particleFilter.pos[:, 1], s=1)
        if z is not None:
            plt.plot(z[0], z[1], 'ro')
        plt.axis([0, 2, -1, 1]) 
        plt.show(block=False) 
    
    
