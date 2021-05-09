import math
import random
from GGA import *

########### XOR TEST ###############

def sigmoid(x):
    if x < 0:
        return math.exp(x)/(math.exp(x)+1)
    return 1/(1+math.exp(-x))


class XOR_NeuralNetwork:
    def __init__(self):
        self.nb_inputs = 2
        self.nb_outs = 1
        self.hidden_layers = 1
        self.hidden_neuron = 2
        self.hidden_weights = [[random.uniform(-2,2) for _ in range(self.nb_inputs)] for _ in range(self.hidden_neuron)] # 4
        self.hidden_biases = [random.uniform(-2,2) for _ in range(self.hidden_neuron)] # 2
        self.outs_weights = [[random.uniform(-2,2) for _ in range(self.hidden_neuron)] for _ in range(self.nb_outs)] # 2
        self.outs_biases = [random.uniform(-2,2) for _ in range(self.nb_outs)] # 1

    def loadPool(self, pool):
        for i in range(len(pool)):
            if i <= 3:
                self.hidden_weights[i//2][i%2] = pool[i]
            elif i <= 5:
                self.hidden_biases[i-4] = pool[i]
            elif i <= 7:
                self.outs_weights[0][i-6] = pool[i]
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

####################  GGA Application ##################

def poolFitness(pool):
    NN = XOR_NeuralNetwork()
    NN.loadPool(pool)
    score = 0
    for a in [0,1]:
        for b in [0,1]:
            expected = a ^ b
            got = NN.forward([a,b])
            score += (1-abs(expected-got[0]))*10
    return score

def genFromParent(p1,p2):
    pool = CROSS.MultiPoint(p1,p2,random.randint(1,10))
    pool = MUTATOR.RandomReset(pool,0.1,[-10,10])
    return pool

def process(nb_pool, iteration=100):
    pools = [POP.RandomInit(9,-1,1) for _ in range(nb_pool)]
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

    NN = XOR_NeuralNetwork()
    NN.loadPool(mx[1])
    score = 0
    for a in [0,1]:
        for b in [0,1]:
            expected = a ^ b
            got = NN.forward([a,b])
            print(a,b," >>> Expected : ", expected, "Got : ", got)

process(500)
