import math
import random
import tkinter as tk

root = tk.Tk()
root.title("Particles in Classical Mechanics")


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
cursor_x = CANVAS_WIDTH/2
cursor_y = CANVAS_HEIGHT/2
MAX_SPEED = 5
HEAVY_RADIUS = 3
MASSIVE_PARTICLE_STRONG_CHARGE = 8
ELECTRON_RADIUS = 2
FORCE_DIST_MODIFIER = 1
electron_orbital_dist = 30
nuclear_particle_spacing = 10

simple_orbitals = tk.BooleanVar()
simple_orbitals.set(True)
strong_force_active = tk.BooleanVar()
electrostatic_force_active = tk.BooleanVar()


class Nucleus:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.members = []


class Particle:
    def __init__(self, id, type, shape, sim_width, sim_height):
        self.type = type
        self.id = id
        if type == "p":  # proton
            self.radius = HEAVY_RADIUS
            self.mass = 1
            self.electrostatic_charge = 1
            self.strong_charge = MASSIVE_PARTICLE_STRONG_CHARGE
            self.energy_level = 0

        if type == "n":  # neutron
            self.radius = HEAVY_RADIUS
            self.mass = 1
            self.electrostatic_charge = 0
            self.strong_charge = MASSIVE_PARTICLE_STRONG_CHARGE
            self.energy_level = 0

        if type == "e":  # electron
            self.radius = ELECTRON_RADIUS
            self.mass = .001
            self.electrostatic_charge = -1
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

        self.electrostatic_interacted = []  #keeps track of what particles this has interacted with electrostatically
        self.strong_interacted = []  #keeps track of what particles this has interacted with strongly

        self.closest_nucleus = None

    def reset(self):
        self.electrostatic_interacted.clear()
        self.strong_interacted.clear()
        self.x_acc = 0
        self.y_acc = 0
        self.closest_nucleus = None

    def find_closes_nucleus(self, nucleus_list):
        if (nucleus_list):
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

    def orbital_simple(self):
        # keep electron far enough away from the nucleus
        #print(f"{self.type=} {self.closest_nucleus=}" )
        if self.type == 'e' and self.closest_nucleus != None:
            dist_to_nucleus_x = self.closest_nucleus.x_pos - self.x_pos
            dist_to_nucleus_y = self.closest_nucleus.y_pos - self.y_pos
            dist_to_nucleus = math.sqrt(dist_to_nucleus_x ** 2 + dist_to_nucleus_y ** 2)
            min_distance = 30 * self.energy_level
            if dist_to_nucleus > 0:
                if dist_to_nucleus < min_distance:
                    min_distance_factor = min_distance / dist_to_nucleus
                    dist_to_nucleus_x = dist_to_nucleus_x * min_distance_factor
                    dist_to_nucleus_y = dist_to_nucleus_y * min_distance_factor
                    self.x_pos = self.closest_nucleus.x_pos - dist_to_nucleus_x
                    self.y_pos = self.closest_nucleus.y_pos - dist_to_nucleus_y
                    #print(f"{min_distance_factor=} {dist_to_nucleus_x=} {dist_to_nucleus_y=}" )

    def orbital(self):
        global simple_orbitals
        if simple_orbitals.get():
            self.orbital_simple()
            return
        # keep electron far enough away from the nucleus
        if self.type == 'e' and self.closest_nucleus != None:
            dist_to_nucleus_x = self.closest_nucleus.x_pos - self.x_pos
            dist_to_nucleus_y = self.closest_nucleus.y_pos - self.y_pos
            dist_to_nucleus = math.sqrt(dist_to_nucleus_x ** 2 + dist_to_nucleus_y ** 2)
            min_distance = 30 * self.energy_level
            if dist_to_nucleus > 0 and dist_to_nucleus < min_distance:  #  > 0 prevents /0 chrashes
                min_distance_factor = min_distance / dist_to_nucleus
                dist_to_nucleus_x = dist_to_nucleus_x * min_distance_factor
                dist_to_nucleus_y = dist_to_nucleus_y * min_distance_factor
                self.x_pos = self.closest_nucleus.x_pos - dist_to_nucleus_x
                self.y_pos = self.closest_nucleus.y_pos - dist_to_nucleus_y
                speed = math.sqrt(self.x_vel ** 2 + self.y_vel ** 2)

                # 2 orbital directions possible. calculate both of them
                tangent_x1 = -dist_to_nucleus_y / dist_to_nucleus
                tangent_y1 = dist_to_nucleus_x / dist_to_nucleus
                tangent_x2 = dist_to_nucleus_y / dist_to_nucleus
                tangent_y2 = -dist_to_nucleus_x / dist_to_nucleus

                # use dot products to figure which orbital direction is closer to original
                dot1 = self.x_vel * tangent_x1 + self.y_vel * tangent_y1
                dot2 = self.x_vel * tangent_x2 + self.y_vel * tangent_y2

                # apply whichever velocity change is smaller
                if dot1 > dot2:
                    self.x_vel, self.y_vel = speed * tangent_x1, speed * tangent_y1
                else:
                    self.x_vel, self.y_vel = speed * tangent_x2, speed * tangent_y2

    def accel(self, x, y):
        self.x_acc += x
        self.y_acc += y


def user_click(event):
    global cursor_x
    global cursor_y
    cursor_x = event.x
    cursor_y = event.y
    print(f"{cursor_x=}, {cursor_y=}")

def delete_all_particles():
    global particles
    for p in particles:
        canvas.delete(p.shape)
        #p.shape
    particles = []


def add_proton():
    global canvas
    global particles
    id = 0
    if particles:
        id = particles[-1].id
        id += 1
    particles.append(Particle(id, 'p',
                              canvas.create_oval(-50, -50, -100, -100, fill='Red'),
                              CANVAS_WIDTH,
                              CANVAS_HEIGHT))
    particles[-1].x_pos = cursor_x + random.randint(-3,3)
    particles[-1].y_pos = cursor_y + random.randint(-3,3)


def add_electron():
    global canvas
    global particles
    id = 0
    if particles:
        id = particles[-1].id
        id += 1
    particles.append(Particle(id, 'e',
                              canvas.create_oval(-50, -50, -100, -100, fill='Blue'),
                              CANVAS_WIDTH,
                              CANVAS_HEIGHT))
    particles[-1].x_pos = cursor_x + random.randint(-3,3)
    particles[-1].y_pos = cursor_y + random.randint(-3,3)


def add_neutron():
    global canvas
    global particles
    id = 0
    if particles:
        id = particles[-1].id
        id += 1
    particles.append(Particle(id, 'n',
                              canvas.create_oval(-50, -50, -100, -100, fill='Yellow'),
                              CANVAS_WIDTH,
                              CANVAS_HEIGHT))
    particles[-1].x_pos = cursor_x + random.randint(-3,3)
    particles[-1].y_pos = cursor_y + random.randint(-3,3)


# make data field at top of window
info_field = tk.Label(root, justify=tk.LEFT)
info_field.grid(row=0, column=0, columnspan=5, sticky='w')

# make canvas to display particles
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
canvas.bind("<Button-1>", user_click)
canvas.grid(row=1, column=0, columnspan=5)
# make cursor to show where new particles will go
cursor = canvas.create_oval(cursor_x-10, cursor_y-10, cursor_x+10, cursor_y+10)

# make buttons to add particles
proton_button = tk.Button(root, text="Add Proton", command=add_proton)
proton_button.grid(row=2, column=1)
electron_button = tk.Button(root, text="Add Electron", command=add_electron)
electron_button.grid(row=3, column=1)
neutron_button = tk.Button(root, text="Add Neutron", command=add_neutron)
neutron_button.grid(row=4, column=1)
clear_button = tk.Button(root, text="Clear All", command=delete_all_particles)
clear_button.grid(row=2, column=0)

#make controls for physics
orbital_toggle = tk.Checkbutton(root, text="Simple orbital Model", variable=simple_orbitals,
                                onvalue=True, offvalue=False)
orbital_toggle.grid(row=2, column=3)
orbital_toggle = tk.Checkbutton(root, text="Electrostatic Force", variable=electrostatic_force_active,
                                onvalue=True, offvalue=False)
orbital_toggle.grid(row=2, column=2)
orbital_toggle = tk.Checkbutton(root, text="Strong Force", variable=strong_force_active,
                                onvalue=True, offvalue=False)
orbital_toggle.grid(row=3, column=2)

particles = []
nuclei = []



def em_interact(p_a, p_b):
    # make sure the particles have not interacted already or are interacting with themselves
    if p_a.id not in p_b.electrostatic_interacted and p_a.id != p_b.id:
        p_a.electrostatic_interacted.append(p_b.id)
        p_b.electrostatic_interacted.append(p_a.id)
        dist_x = abs(p_a.x_pos - p_b.x_pos)
        dist_y = abs(p_a.y_pos - p_b.y_pos)
        distance = math.sqrt(pow(dist_x, 2) + pow(dist_y, 2))

        # negative force is repulsion, positive force is attraction
        force = 0
        if distance > 0:
            force = (p_a.electrostatic_charge * p_b.electrostatic_charge) / pow(distance/FORCE_DIST_MODIFIER, 2)

        # calc total acceleration on the particles
            p_a_accel = force / p_a.mass
            p_b_accel = force / p_b.mass

            if (p_a.x_pos > p_b.x_pos):
                p_a_x_vector = (dist_x / distance) * p_a_accel
                p_b_x_vector = -(dist_x / distance) * p_b_accel
            else:
                p_a_x_vector = -(dist_x / distance) * p_a_accel
                p_b_x_vector = (dist_x / distance) * p_b_accel
            if (p_a.y_pos > p_b.y_pos):
                p_a_y_vector = (dist_y / distance) * p_a_accel
                p_b_y_vector = -(dist_y / distance) * p_b_accel
            else:
                p_a_y_vector = -(dist_y / distance) * p_a_accel
                p_b_y_vector = (dist_y / distance) * p_b_accel
            # apply acceleration
            p_a.accel(p_a_x_vector, p_a_y_vector)
            p_b.accel(p_b_x_vector, p_b_y_vector)


def strong_interact(p_a, p_b):
    # make sure the particles have not interacted already or are interacting with themselves
    if p_a.id not in p_b.strong_interacted and p_a.id != p_b.id:
        min_spacing = p_a.radius + p_b.radius
        p_a.strong_interacted.append(p_b.id)
        p_b.strong_interacted.append(p_a.id)
        dist_x = p_a.x_pos - p_b.x_pos
        dist_y = p_a.y_pos - p_b.y_pos
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
        if distance == 0: return
        norm_x = dist_x / distance
        norm_y = dist_y / distance

        # all forces are negative because all the strong force interactions are attractive
        # with negative acceleration in the vector away from the other particle
        if distance >= min_spacing:
            force = -(p_a.strong_charge * p_b.strong_charge) / pow(distance/FORCE_DIST_MODIFIER, 4)
            # calc total acceleration on the particles
            p_a_accel = force / p_a.mass
            p_b_accel = force / p_b.mass
            p_a_x_vector = norm_x * p_a_accel
            p_a_y_vector = norm_y * p_a_accel
            p_b_x_vector = -norm_x * p_b_accel
            p_b_y_vector = -norm_y * p_b_accel
            # apply acceleration
            p_a.accel(p_a_x_vector, p_a_y_vector)
            p_b.accel(p_b_x_vector, p_b_y_vector)

        #if particles are too close, have them collide and exchange momentum
        if 0 < distance < min_spacing:
            # correct overlap
            overlap_depth = min_spacing - distance

            # move the particles to undo the overlap
            move_x = norm_x * overlap_depth / 2
            move_y = norm_y * overlap_depth / 2
            p_a.x_pos += move_x
            p_a.y_pos += move_y
            p_b.x_pos -= move_x
            p_b.y_pos -= move_y

            #slow partiles a bit to prevent spin of death
            p_a.x_vel *= 1-abs(p_a.x_vel/MAX_SPEED)
            p_a.y_vel *= 1-abs(p_b.y_vel/MAX_SPEED)
            p_b.x_vel *= 1-abs(p_a.x_vel/MAX_SPEED)
            p_b.y_vel *= 1-abs(p_b.y_vel/MAX_SPEED)

            # determine relative velocities
            d_x_vel = p_a.x_vel - p_b.x_vel
            d_y_vel = p_a.y_vel - p_b.y_vel

            # project the velocity on the normal
            dot_vel = d_x_vel * norm_x + d_y_vel * norm_y

            # if velocity is positive the particles are separating and no collision needs to happen
            if dot_vel > 0: return

            # calc impulse (impulse is delta momentum)
            elasticity = 0
            imp = ((1 + elasticity) * dot_vel) / (1 / p_a.mass + 1 / p_b.mass)

            # apply acceleration
            p_a.x_vel += -imp * p_b.mass * norm_x
            p_a.y_vel += -imp * p_b.mass * norm_y
            p_b.x_vel += imp * p_a.mass * norm_x
            p_b.y_vel += imp * p_a.mass * norm_y



def update_particles():
    #display cursor
    global cursor
    canvas.coords(cursor, cursor_x-10, cursor_y-10, cursor_x+10, cursor_y+10)

    proton_count = 0
    electron_count = 0
    neutron_count = 0
    for p in particles:
        if p.type == 'p': proton_count += 1
        if p.type == 'e': electron_count += 1
        if p.type == 'n': neutron_count += 1
    total_charge = proton_count - electron_count
    info_string = (f"Protons {proton_count}\nElectrons {electron_count}\n"
                   f"Neutrons{neutron_count}\nTotal Charge {total_charge}\n")
    global info_field
    info_field.config(text=info_string)

    # find all nuclei
    # TODO this only finds protons. Consider if it is worth it to define nuclei
    global nuclei
    nuclei = []
    for p in particles:
        if p.type == 'p':
            nuclei.append(Nucleus(p.x_pos, p.y_pos))

    # find closest nuclei
    for p in particles:
        if p.type == 'e':
            p.find_closes_nucleus(nuclei)

    # solve Strong interactions
    global strong_force_active
    if strong_force_active.get() == True:
        for p_a in particles:
            for p_b in particles:
                if p_a.strong_charge != 0 and p_b.strong_charge != 0:
                    strong_interact(p_a, p_b)
        # p_a.nucleus_spacing()

    # solve EM interactions
    global electrostatic_force_active
    if electrostatic_force_active.get() == True:
        for p_a in particles:
            for p_b in particles:
                if p_a.electrostatic_charge != 0 and p_b.electrostatic_charge != 0:
                    em_interact(p_a, p_b)
            p_a.orbital()  # keep electrons from falling into nucleus

    for p in particles:
        p.move()
        canvas.coords(p.shape, p.x_pos - p.radius, p.y_pos - p.radius,
                      p.x_pos + p.radius, p.y_pos + p.radius)
        p.reset()

    # TODO replace prototyping execution of next frame
    root.after(20, update_particles)


update_particles()
root.mainloop()
