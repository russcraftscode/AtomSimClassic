import math

MAX_SPEED = 5

class Nucleus:
    def __init__(self, x, y ):
        self.x_pos = x
        self.y_pos = y
        self.members = []

class Particle:
    def __init__(self, id, type, shape, sim_width, sim_height):
        self.type = type
        self.id = id
        if type == "p": # proton
            self.radius = 5
            self.mass = 1
            self.electric_charge = 1
            self.strong_charge = 1
            self.energy_level = 0

        if type == "n": # neutron
            self.radius = 5
            self.mass = 1
            self.electric_charge = 0
            self.strong_charge = 0
            self.energy_level = 0

        if type == "e": # neutron
            self.radius = 3
            self.mass = .001
            self.electric_charge = -1
            self.strong_charge = 0
            self.energy_level = 1

        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

        self.sim_width = sim_width
        self.sim_height = sim_height
        self.shape = shape

        self.interacted_with = []  #keeps track of what particles this has interacted with

        self.closest_nucleus = None

    def reset(self):
        self.interacted_with.clear()
        self.x_acc = 0
        self.y_acc = 0
        self.closest_nucleus = None

    def find_closes_nucleus(self, nucleus_list):
        if(nucleus_list):
            closest_range = 1000000
            for n in nucleus_list:
                dist_to_nucleus_x = n.x_pos - self.x_pos
                dist_to_nucleus_y = n.y_pos - self.y_pos
                dist_to_nucleus = math.sqrt(dist_to_nucleus_x ** 2 + dist_to_nucleus_y ** 2)
                if dist_to_nucleus < closest_range:
                    closest_range = dist_to_nucleus
                    self.closest_nucleus = n

    def move(self):
        #MAX_SPEED = 5
        #if self.type == 'p' or self.type == 'n':
        #    MAX_SPEED = 2
        if self.x_acc > MAX_SPEED: self.x_acc = MAX_SPEED
        if self.y_acc > MAX_SPEED: self.y_acc = MAX_SPEED
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

        # bounce off walls
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

    def orbital(self):
        # keep electron far enough away from the nucleus
        #print(f"{self.type=} {self.closest_nucleus=}" )
        if self.type == 'e' and self.closest_nucleus != None:
            dist_to_nucleus_x = self.closest_nucleus.x_pos - self.x_pos
            dist_to_nucleus_y = self.closest_nucleus.y_pos - self.y_pos
            dist_to_nucleus = math.sqrt(dist_to_nucleus_x ** 2 + dist_to_nucleus_y ** 2)
            #print(f"{self.closest_nucleus.x_pos=}, {self.closest_nucleus.y_pos=} {dist_to_nucleus_x=}, {dist_to_nucleus_y=}" )
            min_distance = 30 * self.energy_level
            #print(f"{dist_to_nucleus=} {dist_to_nucleus_x=} {dist_to_nucleus_y=}" )
            if dist_to_nucleus > 0:
                if dist_to_nucleus < min_distance:
                    min_distance_factor = min_distance / dist_to_nucleus
                    dist_to_nucleus_x = dist_to_nucleus_x * min_distance_factor
                    dist_to_nucleus_y = dist_to_nucleus_y * min_distance_factor
                    self.x_pos = self.closest_nucleus.x_pos - dist_to_nucleus_x
                    self.y_pos = self.closest_nucleus.y_pos - dist_to_nucleus_y
                    #print(f"{min_distance_factor=} {dist_to_nucleus_x=} {dist_to_nucleus_y=}" )

    def accel(self, x, y):
        self.x_acc += x
        self.y_acc += y

