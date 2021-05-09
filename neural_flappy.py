import math
import random
from GGA import *

########### Flappt Neural network ###############

def sigmoid(x):
    if x < 0:
        return math.exp(x)/(math.exp(x)+1)
    return 1/(1+math.exp(-x))


class FNN:
    def __init__(self):
        self.nb_inputs = 4
        self.nb_outs = 1
        self.hidden_layers = 1
        self.hidden_neuron = 2
        self.hidden_weights = [[random.uniform(-2,2) for _ in range(self.nb_inputs)] for _ in range(self.hidden_neuron)] # 8
        self.hidden_biases = [random.uniform(-2,2) for _ in range(self.hidden_neuron)] # 2
        self.outs_weights = [[random.uniform(-2,2) for _ in range(self.hidden_neuron)] for _ in range(self.nb_outs)] # 2
        self.outs_biases = [random.uniform(-2,2) for _ in range(self.nb_outs)] # 1

    def loadPool(self, pool):
        for i in range(len(pool)):
            if i <= 7:
                self.hidden_weights[i//4][i%4] = pool[i]
            elif i <= 9:
                self.hidden_biases[i-8] = pool[i]
            elif i <= 11:
                self.outs_weights[0][i-10] = pool[i]
            else:
                self.outs_biases[i%2] = pool[i]

    def forward(self, input):
         res = []
         for h in range(self.hidden_neuron):
             r = 0
             for i in range(len(input)):
                 r += self.hidden_weights[h][i]*input[i]
             r += self.hidden_biases[h]
             r = sigmoid(r)
             res.append(r)
         outs = []
         for o in range(self.nb_outs):
             r = 0
             for h in range(self.hidden_neuron):
                 r += self.outs_weights[o][h]*res[h]
             r += self.outs_biases[o]
             r = sigmoid(r)
             outs.append(r)
         return outs

################## Flappy Mecanics ###############

Hspeed = 1
Vspeed = 1

def PipeGenerator():
    x = 10
    while True:
        inter = 5
        MX = random.randint(5,10)
        yield [x, MX,MX-inter]
        x += 10

def lineCollision(p1,p2,x,rang):
    a = (p2[1]-p1[1])/(p2[0]-p1[0])
    b = p1[1] - a*p1[0]
    v = a*x+b
    return rang[0] <= v <= rang[1]

def localStateLog(Pipe, flappy):
    print("#"*10)
    for y in range(10):
        pt = int(Pipe[0] - flappy[0])
        if flappy[1] == y:
            print("f",end="")


        if y >= Pipe[1] or y <= Pipe[2]:
            if pt > 0:
                print(" "*(pt-1),"%")
            else:
                print("%")
        else:
            print()

    print("#"*10)


####################  GGA Application ##################

def poolFitness(pool):
    NN = FNN()
    NN.loadPool(pool)
    score = 0
    flappy = [0, 5]
    generator = PipeGenerator()
    currentPipe = generator.__next__()
    while 0 <= flappy[1] <= 10 and score < 100:
        dec = round(NN.forward([flappy[1],currentPipe[0]-flappy[0], currentPipe[1], currentPipe[2]])[0])
        old = list(flappy)
        flappy[0] += Hspeed
        if dec == 1:
            flappy[1] += Hspeed
        else:
            flappy[1] -= Hspeed
        if not currentPipe[2] <= flappy[1] <= currentPipe[1]:#lineCollision(old,flappy,currentPipe[0],[currentPipe[2],currentPipe[1]]):
            score += currentPipe[0] - flappy[0]
            break
        if flappy[0] > currentPipe[0]:
            score += 10
            currentPipe = generator.__next__()
            
    return score

def genFromParent(p1,p2):
    pool = CROSS.MultiPoint(p1,p2,random.randint(1,10))
    pool = MUTATOR.RandomReset(pool,0.1,[-10,10])
    return pool

def process(nb_pool, iteration=100):
    pools = [POP.RandomInit(13,-2,2) for _ in range(nb_pool)]
    for i in range(iteration):
        mx = [-1,None]
        mx2 = [-1,None]
        for pool in pools:
            v = poolFitness(pool)
            if v > mx[0]:
                mx2 = mx
                mx = [v, pool]
            elif v > mx2[0]:
                mx2 = [v, pool]

        if i%10 == 0:
            print("Iteration ", i, " >> TOP 2 : ")
            print(mx)
            print(mx2)
            print(" --===--")
        pools = [genFromParent(mx[1],mx2[1]) for _ in range(nb_pool)]

process(500,200)
