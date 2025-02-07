import math
import random
import tkinter as tk
import Particle


root = tk.Tk()
root.title("Particles in Classical Mechanics")

# build the canvas
canvas_width = 1000
canvas_height = 1000
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# # prototyping stuff
# circle1 = canvas.create_oval(50, 50, 100, 100, fill='blue')
# circle2 = canvas.create_oval(300, 50, 350, 100, fill='red')
# circle3 = canvas.create_oval(300, 50, 350, 100, fill='red')

particles = []

for id in range(10):
    particles.append(Particle.Electron(id,
                                       canvas.create_oval(50, 50, 100, 100, fill='blue'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width/2 + (random.random()-.5) * 300
    particles[-1].y_pos = canvas_height/2 + (random.random()-.5) * 300
    particles[-1].x_vel = random.random()
    particles[-1].y_vel = random.random()

for id in range(10,13):
    particles.append(Particle.Proton(id,
                                       canvas.create_oval(50, 50, 100, 100, fill='Red'),
                                       canvas_width,
                                       canvas_height))
    particles[-1].x_pos = canvas_width/2 + (random.random()-.5) * 300
    particles[-1].y_pos = canvas_height/2 + (random.random()-.5) * 300
    particles[-1].x_vel = 0
    particles[-1].y_vel = 0



# p1 = Particle.Electron(1, circle1, canvas_width, canvas_height)
# p2 = Particle.Electron(2, circle2, canvas_width, canvas_height)
# p3 = Particle.Electron(3, circle3, canvas_width, canvas_height)
#
# particles.append(p1)
# particles.append(p2)
# particles.append(p3)
#
# p1.x_pos = canvas_width/2
# p1.y_pos = canvas_height/2
# p1.x_vel = 0
# p1.y_vel = 0
#
# p2.x_pos = canvas_width/2 + 10
# p2.y_pos = canvas_height/2 +10
# p2.x_vel = 0
# p2.y_vel = 0
#
# p3.x_pos = 0
# p3.y_pos = canvas_height/2
# p3.x_vel = 1
# p3.y_vel = 0



def em_interact(p_a, p_b):
    #make sure the particles have not interacted already or are interacting with themselves
    if p_a.id not in p_b.interacted_with and p_a.id != p_b.id:
        p_a.interacted_with.append(p_b.id)
        p_b.interacted_with.append(p_a.id)
        dist_x = abs(p_a.x_pos - p_b.x_pos)
        dist_y = abs(p_a.y_pos - p_b.y_pos)
        distance = math.sqrt(pow(dist_x,2) + pow(dist_y, 2))

        # negative force is repulsion, positive force is attraction
        force = 0
        if distance > 0:
            force = (p_a.electric_charge * p_b.electric_charge) / pow(distance, 2)

        # calc total acceleration on the particles
        p_a_accel = force/p_a.mass
        p_b_accel = force / p_b.mass
        #print(f"{distance=} a {p_a_accel} b {p_b_accel}") # DEBUG
        # break down acceleration in x,y vectors
        p_a_x_vector = 0
        p_b_x_vector = 0
        p_b_y_vector = 0

        if (p_a.x_pos > p_b.x_pos):
            p_a_x_vector = (dist_x/distance) * p_a_accel
            p_b_x_vector = -(dist_x/distance) * p_b_accel
        else:
            p_a_x_vector = -(dist_x/distance) * p_a_accel
            p_b_x_vector = (dist_x/distance) * p_b_accel
        if (p_a.y_pos > p_b.y_pos):
            p_a_y_vector = (dist_y/distance) * p_a_accel
            p_b_y_vector = -(dist_y/distance) * p_b_accel
        else:
            p_a_y_vector = -(dist_y/distance) * p_a_accel
            p_b_y_vector = (dist_y/distance) * p_b_accel
        # apply acceleration
        p_a.accel(p_a_x_vector, p_a_y_vector )
        p_b.accel(p_b_x_vector, p_b_y_vector)
def move_circles():
    #global p1, p2

    for p_a in particles:
        for p_b in particles:
            em_interact(p_a, p_b)

    for p in particles:
        p.move()
        #print(f"{p.x_vel},{p.y_vel}")
        canvas.coords(p.shape, p.x_pos-p.radius,  p.y_pos-p.radius,
                      p.x_pos+p.radius,  p.y_pos+p.radius)
        p.reset()



    #print(f"{p1.x_pos},{p1.y_pos} {p2.x_pos},{p2.y_pos}")


    # TODO replace prototyping execution of next frame
    root.after(20, move_circles)


move_circles()
root.mainloop()







