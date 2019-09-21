from tkinter import *


class Block:
    def __init__(self, master):
        self.e = Entry(master, width=40)
        self.b = Button(master, text="Преобразовать")
        self.l = Label(master, bg='black', fg='white', width=40)
        self.b['command'] = self.strToSortlist
        self.e.pack()
        self.b.pack()
        self.l.pack()

    def strToSortlist(self):
        s = self.e.get()
        s = s.split()
        s.sort()
        self.l['text'] = ' '.join(s)

root = Tk()

first_block = Block(root)

root.mainloop()

