from tkinter import *

root = Tk()

c = Canvas(root, width=500, height=500, bg='white')
c.pack()

c.create_line(10, 10, 190, 50)

c.create_line(100, 180, 100, 60, fill='green',
              width=5, arrow=LAST, dash=(10, 2),
              activefill='lightgreen',
              arrowshape="10 20 10")

c.create_rectangle(10, 210, 190, 260)

c.create_rectangle(60, 280, 140, 390, fill='yellow', outline='green',
                   width=3, activedash=(5, 4))

c.create_oval(350, 10, 450, 110, width=2)
c.create_oval(310, 120, 490, 190, fill='grey70', outline='white')

root.mainloop()
