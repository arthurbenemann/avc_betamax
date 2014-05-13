from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

fig = plt.figure("particleFilter")
plt.show(block=False)
plt.hold(True)


class Plot:
    def newData(self, z, kalman):        
        plt.figure("Kalman ZX")
        plt.clf()
        plt.hold(True)
        plt.plot(kalman.x[0], kalman.x[2], 'bo')
        if (z is not None):
            plt.plot(z[0], z[2], 'ro', kalman.x[0], kalman.x[2], 'bo')
        
        if (kalman.P.max() <= 1):
            plt.gca().add_patch(Ellipse(xy=(kalman.x[0], kalman.x[2]), width=kalman.P[0, 0], height=kalman.P[2, 2], edgecolor='b', fc='None', lw=2))
            
        plt.axis([0, 2, -1, 1])            
        plt.draw()
        plt.show(block=False)
        

    

    def newParticleFilterData(self, z, particleFilter):
        plt.figure("particleFilter")
        plt.clf()
        plt.subplot(311)
        plt.title("ZX")
        plt.axis([0, 1, -0.3, 0.3])
        # estimate = particleFilter.mean()
        # plt.plot(estimate[0], estimate[2], 'bo')
        plt.scatter(particleFilter.pos[:, 2], particleFilter.pos[:, 0], s=1)
        if z is not None:
            plt.plot(z[2], z[0], 'ro') 
        
        plt.subplot(312)
        plt.title("ZY")
        plt.axis([0, 1, -0.3, 0.3])
        # estimate = particleFilter.mean()
        # plt.plot(estimate[0], estimate[2], 'bo')
        plt.scatter(particleFilter.pos[:, 2], particleFilter.pos[:, 1], s=1)
        if z is not None:
            plt.plot(z[2], z[1], 'ro') 
        
        plt.subplot(313)
        plt.title("XY")
        plt.axis([-0.3, 0.3, -0.3, 0.3])
        # estimate = particleFilter.mean()
        # plt.plot(estimate[0], estimate[2], 'bo')
        plt.scatter(particleFilter.pos[:, 0], particleFilter.pos[:, 1], s=1)
        if z is not None:
            plt.plot(z[0], z[1], 'ro')
            
        #plot3D()
            
        plt.draw() 
    
    
    def plot3D(self,particleFilter,z):
        plt.figure("3D")
        ax = Axes3D(fig)
        #plt.axis([0, 0.5, -0.3, 0.3])
        # estimate = particleFilter.mean()
        # plt.plot(estimate[0], estimate[2], 'bo')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim3d(-0.3, 0.3)
        ax.set_ylim3d(-0.3, 0.3)
        ax.set_zlim3d(0, 0.5)        
        ax.scatter(particleFilter.pos[:, 0], particleFilter.pos[:, 1], particleFilter.pos[:, 2])
        if z is not None:
            plt.scatter(z[0], z[1], z[1], 0) 
        plt.show(block=False)
