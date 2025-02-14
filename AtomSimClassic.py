import math
import random
import tkinter as tk
import Particle

root = tk.Tk()
root.title("Particles in Classical Mechanics")

def add_proton():
    global canvas
    global particles
    id = 0
    if particles:
        id = particles[-1].id
        id += 1
    particles.append(Particle.Particle(id, 'p',
                                       canvas.create_oval(-50, -50, -100, -100, fill='Red'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width / 2 + (random.random() - .5) * 50
    particles[-1].y_pos = canvas_height / 2 + (random.random() - .5) * 50

def add_electron():
    global canvas
    global particles
    id = 0
    if particles[0]:
        id = particles[-1].id
        id += 1
    particles.append(Particle.Particle(id, 'e',
                                       canvas.create_oval(-50, -50, -100, -100, fill='Blue'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width / 2 + (random.random() - .5) * 50
    particles[-1].y_pos = canvas_height / 2 + (random.random() - .5) * 50

def add_neutron():
    global canvas
    global particles
    id = 0
    if particles[0]:
        id = particles[-1].id
        id += 1
    particles.append(Particle.Particle(id, 'n',
                                       canvas.create_oval(-50, -50, -100, -100, fill='Yellow'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width / 2 + (random.random() - .5) * 50
    particles[-1].y_pos = canvas_height / 2 + (random.random() - .5) * 50

# make data field at top of window
info_field = tk.Label(root, justify=tk.LEFT)
info_field.grid(row=0, column=0, columnspan=5, sticky='w')

# make canvas to display animation
canvas_width = 800
canvas_height = 500
electron_count = 50
proton_count = 0
neutron_count = 0
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
#canvas.pack()
canvas.grid(row=1,column=0, columnspan=5)

# make buttons to add particles
proton_button = tk.Button(root, text="Add Proton", command = add_proton)
proton_button.grid(row = 2, column = 0)
proton_button = tk.Button(root, text="Add Electron", command = add_electron)
proton_button.grid(row = 3, column = 0)
proton_button = tk.Button(root, text="Add Neutron", command = add_neutron)
proton_button.grid(row = 4, column = 0)

particles = []
nuclei = []

if False:
    particles.append(Particle.Particle(id, 'p', canvas.create_oval(50, 50, 100, 100, fill='Red'), canvas_width, canvas_height))
    particles[-1].x_pos = 300
    particles[-1].y_pos = 300
    id += 1

    particles.append(Particle.Particle(id, 'p',canvas.create_oval(50, 50, 100, 100, fill='Red'), canvas_width, canvas_height))
    particles[-1].x_pos = 350
    particles[-1].y_pos = 350
    id += 1

    particles.append(Particle.Particle(id, 'e', canvas.create_oval(50, 50, 100, 100, fill='blue'), canvas_width, canvas_height))
    particles[-1].x_pos = 300
    particles[-1].y_pos = 350
    id += 1

    particles.append(Particle.Particle(id, 'e',canvas.create_oval(50, 50, 100, 100, fill='blue'), canvas_width, canvas_height))
    particles[-1].x_pos = 310
    particles[-1].y_pos = 340
    id += 1



def em_interact(p_a, p_b):
    # make sure the particles have not interacted already or are interacting with themselves
    if p_a.id not in p_b.interacted_with and p_a.id != p_b.id:
        p_a.interacted_with.append(p_b.id)
        p_b.interacted_with.append(p_a.id)
        dist_x = abs(p_a.x_pos - p_b.x_pos)
        dist_y = abs(p_a.y_pos - p_b.y_pos)
        distance = math.sqrt(pow(dist_x, 2) + pow(dist_y, 2))

        # negative force is repulsion, positive force is attraction
        force = 0
        if distance > 0:
            force = (p_a.electric_charge * p_b.electric_charge) / pow(distance, 2)
            # calc total acceleration on the particles
            p_a_accel = force / p_a.mass
            p_b_accel = force / p_b.mass
            # print(f"{distance=} a {p_a_accel} b {p_b_accel}") # DEBUG
            # break down acceleration in x,y vectors
            p_a_x_vector = 0
            p_b_x_vector = 0
            p_b_x_vector = 0
            p_b_y_vector = 0

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


def update_particles():
    proton_count = 0
    electron_count = 0
    neutron_count = 0
    for p in particles:
        if p.type == 'p': proton_count += 1
        if p.type == 'e': electron_count += 1
        if p.type == 'n': neutron_count += 1
    # TODO: Make this account for differing proton charges
    total_charge = proton_count - electron_count
    info_string = (f"Protons {proton_count}\nElectrons {electron_count}\n"
                   f"Neutrons{neutron_count}\nTotal Charge {total_charge}\n")
    global info_field
    info_field.config(text=info_string)

    # find all nuclei
    global nuclei
    nuclei = []
    for p in particles:
        if p.type == 'p':
            nuclei.append(Particle.Nucleus(p.x_pos, p.y_pos))

    # find closest nuclei
    for p in particles:
        if p.type == 'e':
            p.find_closes_nucleus(nuclei)

    # solve EM interactions
    for p_a in particles:
        for p_b in particles:
            em_interact(p_a, p_b)

    # solve orbitals
    for p in particles:
        p.orbital()

    for p in particles:
        p.move()
        canvas.coords(p.shape, p.x_pos - p.radius, p.y_pos - p.radius,
                      p.x_pos + p.radius, p.y_pos + p.radius)
        p.reset()

    # TODO replace prototyping execution of next frame
    root.after(20, update_particles)


update_particles()
root.mainloop()



