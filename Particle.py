import math


class Electron:
    def __init__(self, id, shape, sim_width, sim_height):
        self.id = id
        self.radius = 5
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

        self.mass = .001
        self.electric_charge = -1

        self.sim_width = sim_width
        self.sim_height = sim_height
        self.shape = shape

        self.interacted_with = []  #keeps track of what particles this has interacted with

        self.closest_nucleus_x = 0
        self.closest_nucleus_y = 0
        self.energy_level = 1

    def reset(self):
        self.interacted_with.clear()
        self.x_acc = 0
        self.y_acc = 0

    def move(self):
        MAX_SPEED = 5
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc

        # keep under max speed
        speed = math.sqrt(self.x_vel ** 2 + self.y_vel ** 2)
        speed_reduction_factor = speed / MAX_SPEED
        if speed_reduction_factor > 1:
            self.x_vel = self.x_vel / speed_reduction_factor
            self.y_vel = self.y_vel / speed_reduction_factor

        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        # keep electron far enough away from the nucleus
        dist_to_nucleus_x = self.closest_nucleus_x - self.x_pos
        dist_to_nucleus_y = self.closest_nucleus_y - self.y_pos
        dist_to_nucleus = math.sqrt(dist_to_nucleus_x ** 2 + dist_to_nucleus_y ** 2)
        min_distance = 30 * self.energy_level
        #print(f"{dist_to_nucleus=} {dist_to_nucleus_x=} {dist_to_nucleus_y=}" )
        if dist_to_nucleus > 0:
            if dist_to_nucleus < min_distance:
                min_distance_factor = min_distance / dist_to_nucleus
                dist_to_nucleus_x = dist_to_nucleus_x * min_distance_factor
                dist_to_nucleus_y = dist_to_nucleus_y * min_distance_factor
                self.x_pos = self.closest_nucleus_x - dist_to_nucleus_x
                self.y_pos = self.closest_nucleus_y - dist_to_nucleus_y
                #print(f"{min_distance_factor=} {dist_to_nucleus_x=} {dist_to_nucleus_y=}" )

        if self.x_pos < 0:
            self.x_pos = 0
            self.x_vel = -self.x_vel
        if self.x_pos > self.sim_width:
            self.x_pos = self.sim_width
            self.x_vel = -self.x_vel
        if self.y_pos < 0:
            self.y_pos = 0
            self.y_vel = -self.y_vel
        if self.y_pos > self.sim_height:
            self.y_pos = self.sim_height
            self.y_vel = -self.y_vel

    def accel(self, x, y):
        self.x_acc += x
        self.y_acc += y


class Proton:
    def __init__(self, id, shape, sim_width, sim_height):
        self.id = id
        self.radius = 10
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

        self.mass = .1
        self.electric_charge = 1

        self.sim_width = sim_width
        self.sim_height = sim_height
        self.shape = shape

        self.interacted_with = []  #keeps track of what particles this has interacted with

    def reset(self):
        self.interacted_with.clear()
        self.x_acc = 0
        self.y_acc = 0

    def move(self):
        MAX_SPEED = 5
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc

        speed = math.sqrt(self.x_vel ** 2 + self.y_vel ** 2)
        speed_reduction_factor = speed / MAX_SPEED
        if speed_reduction_factor > 1:
            self.x_vel = self.x_vel / speed_reduction_factor
            self.y_vel = self.y_vel / speed_reduction_factor

        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        if self.x_pos < 0:
            self.x_pos = 0
            self.x_vel = -self.x_vel
        if self.x_pos > self.sim_width:
            self.x_pos = self.sim_width
            self.x_vel = -self.x_vel
        if self.y_pos < 0:
            self.y_pos = 0
            self.y_vel = -self.y_vel
        if self.y_pos > self.sim_height:
            self.y_pos = self.sim_height
            self.y_vel = -self.y_vel

    def accel(self, x, y):
        self.x_acc += x
        self.y_acc += y
