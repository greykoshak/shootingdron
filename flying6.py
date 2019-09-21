from tkinter import *

root = Tk()
c = Canvas(root, width=300, height=200, bg="white")
c.pack()

ball = c.create_oval(0, 100, 40, 140, fill='green')


def motion():
    k = 1
    c.move(ball, k, 0)
    if c.coords(ball)[2] < 300:
        root.after(10, motion)


motion()

root.mainloop()
