class Electron:
    def __init__(self, id,  shape, sim_width, sim_height):
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

        self.interacted_with = [] #keeps track of what particles this has interacted with

    def reset(self):
        self.interacted_with.clear()
        self.x_acc = 0
        self.y_acc = 0

    def move(self):
        self.x_vel += self.x_acc
        self.x_pos += self.x_vel
        self.y_vel += self.y_acc
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

class Proton:
    def __init__(self, id,  shape, sim_width, sim_height):
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

        self.interacted_with = [] #keeps track of what particles this has interacted with

    def reset(self):
        self.interacted_with.clear()
        self.x_acc = 0
        self.y_acc = 0

    def move(self):
        self.x_vel += self.x_acc
        self.x_pos += self.x_vel
        self.y_vel += self.y_acc
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