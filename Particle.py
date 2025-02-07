class Electron:
    def __init__(self, sim_width, sim_height):
        self.radius = 1
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

        self.sim_width = sim_width
        self.sim_height = sim_height

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