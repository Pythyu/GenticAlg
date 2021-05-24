from tkinter import *
import random

def trace_line(map, p1,p2, thick):
    if p1[0] > p2[0]:
        p1, p2 = p2, p1
    a = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p1[1] - (a * p1[0])
    f = lambda x : a*x+b
    for x in range(p1[0],p2[0]+1):
        ry = int(f(x))
        rx = x
        for yi in range(ry-thick,ry+thick):
            for xi in range(rx-thick, rx+thick):
                try:
                    map[yi][xi] = 1
                except:
                    pass


def gen_map(width,height,nb_pts=10):
    map = [[0 for _ in range(width)] for _ in range(height)]
    init = [random.randint(0,width),random.randint(0,height)]
    p = init
    for _ in range(nb_pts):
        n = [random.randint(0,width),random.randint(0,height)]
        trace_line(map, p, n, 2)
        p, n = n, p
    trace_line(map, p, init, 2)
    for x in range(width):
        map[0][x] = 0
        map[height-1][x] = 0
    for y in range(height):
        map[y][0] = 0
        map[y][width-1] = 0
    return map

carte = gen_map(80,60,10)

class App:
    def __init__(self):
        self.w = 800
        self.h = 600
        self.tk = Tk()
        self.can = Canvas(width=self.w,height=self.h)
        self.can.pack()
        self.show()
        self.tk.mainloop()

    def show(self):
        for y in range(60):
            for x in range(80):
                if carte[y][x] == 1:
                    self.can.create_rectangle(x*10,y*10,(x+1)*10,(y+1)*10,fill="white",outline="white")
                else:
                    self.can.create_rectangle(x*10,y*10,(x+1)*10,(y+1)*10,fill="gray",outline="gray")

App()
