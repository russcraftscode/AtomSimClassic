import tkinter as tk

root = tk.Tk()
root.title("Particles in Classical Mechanics")

# build the canvas
canvas_width = 400
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# prototyping stuff
circle1 = canvas.create_oval(50, 50, 100, 100, fill='blue')
circle2 = canvas.create_oval(300, 50, 350, 100, fill='red')

dx1, dy1 = 2, 2
dx2, dy2 = -2, 3


def move_circles():
    global dx1, dy1, dx2, dy2

    canvas.move(circle1, dx1, dy1)
    canvas.move(circle2, dx2, dy2)

    x1, y1, x2, y2 = canvas.coords(circle1)
    a1, b1, a2, b2 = canvas.coords(circle2)

    if x1 <= 0 or x2 >= canvas_width:
        dx1 = -dx1
    if y1 <= 0 or y2 >= canvas_height:
        dy1 = -dy1

    if a1 <= 0 or a2 >= canvas_width:
        dx2 = -dx2
    if b1 <= 0 or b2 >= canvas_height:
        dy2 = -dy2

    # TODO replace prototyping execution of next frame
    root.after(20, move_circles)


root.mainloop()
