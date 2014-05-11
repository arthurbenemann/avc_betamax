
import numpy as np

class Kalman:
    A = np.array([[1, 0], [0, 1]])  # Process model
    H = np.array([[1, 0], [0, 1]])  # Measurament model
    Q = np.eye(2) * 0.002  # Process covariance
    R = np.array([[5, 0], [0, 1]])  # Measurament covariance
    
    x = np.array([0, 0])  # Initial pos
    P = np.eye(2) * 100000000  # Initial Covariance

    def predict(self):
        self.xp = self.A.dot(self.x)
        self.Pp = self.A.dot(self.P.dot(self.A.T)) + self.Q
        
    def update(self, z):
        self.predict()
        if z is None:
            self.P = self.Pp
        else:
            self.K = self.Pp.dot(self.H.T.dot(np.linalg.inv(self.H.dot(self.Pp.dot(self.H.T)) + self.R)))        
            self.x = self.xp + self.K.dot(z - self.H.dot(self.xp))
            self.P = self.Pp - self.K.dot(self.H.dot(self.Pp))
