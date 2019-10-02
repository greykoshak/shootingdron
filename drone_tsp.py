from tkinter import *

import numpy as np
from numpy import sqrt


class FindRoot:
    def __init__(self):
        self.coord = list()
        self.out = list()
        print("FindRoot: ", self.coord)

    def set_coord(self, coord: list):
        self.coord = coord

    def computing(self):
        X = [k[0] for k in self.coord]
        Y = [k[1] for k in self.coord]

        n = len(X)
        RS, RW, RIB, s = list(), list(), list(), list();

        for ib in np.arange(0, n, 1):
            M = np.zeros([n, n])
            for i in np.arange(0, n, 1):
                for j in np.arange(0, n, 1):
                    if i != j:
                        M[i, j] = sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
                    else:
                        M[i, j] = float('inf')

            way = list()
            way.append(ib)

            for i in np.arange(1, n, 1):
                s = list()
                for j in np.arange(0, n, 1):
                    s.append(M[way[i - 1], j])
                way.append(s.index(min(s)))
                for j in np.arange(0, i, 1):
                    M[way[i], way[j]] = float('inf')
                    M[way[i], way[j]] = float('inf')
            S = sum([sqrt((X[way[i]] - X[way[i + 1]]) ** 2 + (Y[way[i]] - Y[way[i + 1]]) ** 2)
                     for i in np.arange(0, n - 1, 1)]) + sqrt((X[way[n - 1]] - X[way[0]]) ** 2 +
                                                              (Y[way[n - 1]] - Y[way[0]]) ** 2)
            RS.append(S)
            RW.append(way)
            RIB.append(ib)

        S = min(RS)
        way = RW[RS.index(min(RS))]
        ib = RIB[RS.index(min(RS))]

        X1 = [X[way[i]] for i in np.arange(0, n, 1)]
        Y1 = [Y[way[i]] for i in np.arange(0, n, 1)]

        self.out = [tuple(tup) for tup in zip(X1, Y1)]

    def get_root(self):
        self.computing()
        return self.out


class Drone:
    def __init__(self, canvas):
        self.canvas = canvas
        self.full_charge = 600  # Полный заряд дрона
        self.delta_e_flying = 1  # Расход энергии на единицу пройденного расстояния
        self.delta_e_shooting = 4  # Расход энергии на рдин снимок

    # l - кортеж, координаты начальной точки (x1, y1) и конечной точки (x2, y2)
    # l = (x1, y1, x2, y2)
    # Возвращает расстояние между точками
    @staticmethod
    def distance(l: tuple) -> float:
        return (abs(l[2] - l[0]) ** 2 + abs(l[3] - l[1]) ** 2) ** 0.5

    # Максимальное расстояние полета (туда и обратно) + один снимок
    # Зависит от начальной энергии и расхода на единицу полета и снимок
    # Возвращает радиус круга
    def max_radius(self) -> float:
        max_distance = (self.full_charge - self.delta_e_shooting) / self.delta_e_flying
        return max_distance / 2

    def get_full_charge(self):
        return self.full_charge

    def set_full_charge(self, new_value):
        self.full_charge -= new_value
        print("Остаток энергии: {:5.2f}".format(self.get_full_charge()))
        return


class DefCoord:
    points = [(800, 400), (500, 300), (900, 500), (900, 400), (700, 100), (500, 500)]

    @classmethod
    def get_area(cls):
        return cls.points


class CalcRoot:
    def __init__(self, obj_drone, coord: list, obj):
        self.my_drone = obj_drone
        self.coord = coord
        self.obj = obj
        obj_drone.canvas.bind('<Button-1>', self.drawing_root)

    def drawing_point(self, x, y, color):
        self.my_drone.canvas.create_oval(x - 3, y + 3, x + 3, y - 3, fill=color)

    def drawing_line(self, x1, y1, x2, y2, color):
        self.my_drone.canvas.create_line(x1, y1, x2, y2, dash=(4, 2), fill=color)

    def view_points(self):
        for point in self.coord:
            self.drawing_point(point[0], point[1], "blue")

    def drawing_root(self, event):
        temp_x = int(event.x)
        temp_y = int(event.y)
        self.drawing_point(temp_x, temp_y, "red")
        self.my_drone.canvas.bind('<Button-1>', "")
        self.coord.append((temp_x, temp_y))
        print("drawing_root: ", self.coord)
        self.obj.set_coord(self.coord)
        new_root = self.obj.get_root()
        new_root.append(new_root[0])

        total = 0

        for i in range(len(new_root)):
            x1 = new_root[i][0]
            y1 = new_root[i][1]

            if i == len(new_root)-1:
                x2 = new_root[0][0]
                y2 = new_root[0][1]
            else:
                x2 = new_root[i + 1][0]
                y2 = new_root[i + 1][1]

            self.drawing_line(x1, y1, x2, y2, "blue")
            total += self.my_drone.distance((x1, y1, x2, y2))
        print("Total distance: {:7.2f}".format(total))


def main():
    root = Tk()
    root.title("Area Shooting")

    can = Canvas(root, width=1400, height=820, bg="lightgreen")
    can.pack(fill='both', expand=True)

    my_drone = Drone(can)
    print("Радиус: {}, Энергии: {}".format(my_drone.max_radius(), my_drone.get_full_charge()))

    # Получить массив координат для съемки
    coord = DefCoord.get_area()

    r = FindRoot()  # Решение задачи комивояжера

    obj = CalcRoot(my_drone, coord, r)
    obj.view_points()

    root.mainloop()


if __name__ == '__main__':
    main()
