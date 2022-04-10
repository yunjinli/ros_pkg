import numpy as np

class DiffDriveModel:

    def __init__(self):
        pass
    def compute_wheel_velocity(self, linear_vel, angular_vel):
        A = np.array([[0.5 * self.wheel_diameter / 2, 0.5 * self.wheel_diameter / 2],
            [0.5 * 1 / self.wheel_seperation * self.wheel_diameter / 2, -0.5 * 1 / self.wheel_seperation * self.wheel_diameter / 2]])
        b = np.array([[linear_vel], 
            [angular_vel]])
        x = np.dot(np.linalg.inv(A), b)
        return x[0], x[1]
    def set_wheel_seperation(self, wheel_seperation):
        self.wheel_seperation = wheel_seperation
    def set_wheel_diameter(self, wheel_diameter):
        self.wheel_diameter = wheel_diameter
    

