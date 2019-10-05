from tkinter import *

import const
from area import DefCoord
from tsp import FindRoot

const.BASE = ()


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


class DefineArea:
    def __init__(self, obj_drone):
        self.my_drone = obj_drone
        self.top_left = ()
        self.bottom_right = ()
        obj_drone.canvas.bind('<Button-1>', self.set_area)

    def set_area(self, event, color="blue"):
        self.top_left = (int(event.x), int(event.y))
        print("Point: {:5.2f} {:5.2f}".format(event.x, event.y))

        while int(event.x) < self.top_left[0] or int(event.y) < self.top_left[1]:
            print("Point: {:5.2f} {:5.2f}".format(event.x, event.y))
            pass

        self.bottom_right = (int(event.x), int(event.y))

        self.my_drone.canvas.create_rectangle(self.top_left[0], self.top_left[1],
                                              self.bottom_right[0], self.bottom_right[1], fill=color)


# Отображение маршрута после решения задачи комивояжера
class CalcRoot:
    def __init__(self, obj_drone, coord: list, obj):
        self.my_drone = obj_drone
        self.coord = coord
        self.obj = obj
        obj_drone.canvas.bind('<Button-1>', self.drawing_root)

    def drawing_point(self, x, y, color):
        self.my_drone.canvas.create_oval(x - 3, y + 3, x + 3, y - 3, fill=color)

    def drawing_line(self, x1, y1, x2, y2, color):
        self.my_drone.canvas.create_line(x1, y1, x2, y2, dash=(4, 2), arrow=LAST, fill=color)

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
        # new_root.append(new_root[0])

        total = 0

        for i in range(len(new_root)):
            x1 = new_root[i][0]
            y1 = new_root[i][1]

            if i == len(new_root) - 1:
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
    # print("Радиус: {}, Энергии: {}".format(my_drone.max_radius(), my_drone.get_full_charge()))

    # Определить область съемки
    DefineArea(my_drone)

    # Получить массив координат для съемки
    # area = DefCoord((300, 300, 500, 500))
    # coord = area.get_area()
    #
    # r = FindRoot()  # Решение задачи комивояжера
    #
    # obj = CalcRoot(my_drone, coord, r)
    # obj.view_points()

    root.mainloop()


if __name__ == '__main__':
    main()
