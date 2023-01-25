from math import pi, sin, cos

class Pose:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.x_dot = 0
        self.y_dot = 0
        self.theta_dot = 0

class Odometry:
    def __init__(self):
        self.left_encoder = 0
        self.prev_left_encoder = 0
        self.right_encoder = 0
        self.prev_right_encoder = 0
        self.pose = Pose()
        self.last_time = 0

    def set_wheel_seperation(self, wheel_seperation):
        self.wheel_seperation = wheel_seperation

    def set_wheel_diameter(self, wheel_diameter):
        self.wheel_diameter = wheel_diameter

    def set_time(self, new_time):
        self.last_time = new_time
        
    def read_left_encoder(self, rad):
        self.left_encoder = rad

    def read_right_encoder(self, rad):
        self.right_encoder = rad

    def get_travel_dist(self, delta, radius):
        return delta * radius

    def update(self, new_time):
        left_traveled = self.get_travel_dist(self.left_encoder - self.prev_left_encoder, self.wheel_diameter / 2) 
        right_traveled = self.get_travel_dist(self.right_encoder - self.prev_right_encoder, self.wheel_diameter / 2) 
        delta_time = new_time - self.last_time

        delta_traveled = (left_traveled + right_traveled) / 2
        delta_theta = (right_traveled - left_traveled) / self.wheel_seperation

        if right_traveled == left_traveled:
            delta_x = left_traveled*cos(self.pose.theta)
            delta_y = left_traveled*sin(self.pose.theta)
        else:
            r = delta_traveled / delta_theta # (rad) x r = Perimeter

            # Find the instantaneous center of curvature (ICC).
            icc_x = self.pose.x - r * sin(self.pose.theta)
            icc_y = self.pose.y + r * cos(self.pose.theta)

            delta_x = cos(delta_theta) * (self.pose.x - icc_x) \
                - sin(delta_theta) * (self.pose.y - icc_y) \
                + icc_x - self.pose.x

            delta_y = sin(delta_theta) * (self.pose.x - icc_x) \
                + cos(delta_theta) * (self.pose.y - icc_y) \
                + icc_y - self.pose.y

        self.pose.x += delta_x
        self.pose.y += delta_y
        self.pose.theta = (self.pose.theta + delta_theta) % (2 * pi)
        self.pose.x_dot = delta_traveled / delta_time if delta_time > 0 else 0.
        self.pose.y_dot = 0
        self.pose.theta_dot = delta_theta / delta_time if delta_time > 0 else 0.

        self.last_time = new_time
        self.prev_left_encoder = self.left_encoder
        self.prev_right_encoder = self.right_encoder

    def get_pose(self):
        return self.pose

    def set_pose(self, new_pose):
        self.pose = new_pose