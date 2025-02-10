import math
import random
import tkinter as tk
import Particle

root = tk.Tk()
root.title("Particles in Classical Mechanics")

# build the canvas
canvas_width = 800
canvas_height = 600
electron_count = 50
proton_count = 50
neutron_count = 10
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

particles = []
nuclei = []

id = 0;
for p in range(electron_count):
    particles.append(Particle.Particle(id, 'e',
                                       canvas.create_oval(50, 50, 100, 100, fill='blue'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width / 2 + (random.random() - .5) * 300
    particles[-1].y_pos = canvas_height / 2 + (random.random() - .5) * 300
    particles[-1].x_vel =  random.randint(-2,2)
    particles[-1].y_vel = random.randint(-2,2)
    id += 1

for p in range(electron_count, proton_count + electron_count):
    particles.append(Particle.Particle(id, 'p',
                                       canvas.create_oval(50, 50, 100, 100, fill='Red'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width / 2 + (random.random() - .5) * 400
    particles[-1].y_pos = canvas_height / 2 + (random.random() - .5) * 400
    particles[-1].x_vel = random.randint(-2,2)
    particles[-1].y_vel = random.randint(-2,2)
    id += 1

for p in range(proton_count + electron_count, proton_count + electron_count + neutron_count):
    particles.append(Particle.Particle(id, 'n',
                                       canvas.create_oval(50, 50, 100, 100, fill='Yellow'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width / 2 + (random.random() - .5) * 400
    particles[-1].y_pos = canvas_height / 2 + (random.random() - .5) * 400
    particles[-1].x_vel = random.randint(-2,2)
    particles[-1].y_vel = random.randint(-2,2)
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


def move_particles():
    # global p1, p2

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

    # solve EM interations
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
    root.after(20, move_particles)


move_particles()
root.mainloop()
