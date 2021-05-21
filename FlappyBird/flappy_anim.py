from tkinter import *
import ast

def file_line_reader(file):
    for line in file.readlines():
        yield line

def height_converter(x):
    return (256/-10)*x + 256



class Application:
    def __init__(self):
        self.flappy_pos = [50,50]
        self.next_pipe = None
        self.w = 144*8
        self.h = 256
        self.file = open("flappy_log.flap","r")
        self.line_gen = file_line_reader(self.file)
        self.tk = Tk()
        self.load_textures()
        self.can = Canvas(width=self.w,height=self.h)
        self.can.create_image(0,0, image = self.bg_img)
        self.can.pack()

        self.update()


        self.tk.mainloop()

    def load_textures(self):
        self.flappy_img = PhotoImage(file="imgs/flappy.gif")
        self.bg_img = PhotoImage(file="imgs/bg.gif")
        self.pipe_up_img = PhotoImage(file="imgs/pipe_up.gif")
        self.pipe_down_img = PhotoImage(file="imgs/pipe_down.gif")
    def update(self):
        self.can.delete('all')
        try:
            line = self.line_gen.__next__()
            if line[0:3] == "POS":
                # Very BAD design : this code is for demo only
                self.flappy_pos = ast.literal_eval(line[4:])
                #print(self.flappy_pos)
                self.flappy_pos[0] = 2*self.flappy_pos[0]
                self.flappy_pos[1] = height_converter(self.flappy_pos[1])
                #print(self.flappy_pos)
            elif line[0:4] == "PIPE":
                self.next_pipe = ast.literal_eval(line[5:])
        except:
            pass

        for i in range(8):
            self.can.create_image(144*i,0, image = self.bg_img)
        self.can.create_line(self.next_pipe[0]*2,0,self.next_pipe[0]*2,height_converter(self.next_pipe[1]))
        self.can.create_line(self.next_pipe[0]*2,256,self.next_pipe[0]*2,height_converter(self.next_pipe[2]))
        self.can.create_image(self.flappy_pos[0],self.flappy_pos[1],anchor="center",image=self.flappy_img)
        self.can.create_image
        self.tk.after(50, self.update)

app = Application()
