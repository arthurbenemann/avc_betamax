import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

class Plot:

    # Display the plot
    fig = plt.figure()
    plt.show(block=False)
    plt.hold(False)

    def newData(self, z, x, P):
        if (z is None):
            plt.plot(x[0], x[1], 'bo')
        else:
            plt.plot(z[0], z[1], 'ro', x[0], x[1], 'bo')
        
        if (P.max() <= 1):
            plt.gca().add_patch(Ellipse(xy=(x[0], x[1]), width=P[0, 0], height=P[1, 1], edgecolor='b', fc='None', lw=2))
            
        plt.axis([0, 2, -1, 1])            
        plt.draw()
