import math
import random
import numpy as np
from GGA import *

####################  Gold Miner      ##################

WORLD_BORDER = 15

def func(x):
    if x <= 6:
        return 1
    elif x <= 8:
        return -x + 7
    elif x <= 13:
        return x - 9
    elif x <= 19:
        return -x + 15
    elif x <= 25:
        return x - 22
    elif x <= 28:
        return -x + 28
    else:
        return 0

real_min = min([func(i) for i in range(WORLD_BORDER*2)])



####################  GGA Application ##################

def poolFitness(pool):
    return 10 - abs(func(pool[0]) - real_min)

def genFromParent(p1,p2):
    pool = CROSS.MultiPoint(p1,p2,random.randint(1,10))
    pool = MUTATOR.RandomIncrement(pool,0.8,1)
    return pool

def process(nb_pool, iteration=100):
    pools = [[random.uniform(0,WORLD_BORDER)] for _ in range(nb_pool)]
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

    print("Attended Min : ", real_min)
    print("Glouton Min : ", func(mx[1][0]))
    print("A fix would be to change our strategy by inhancing the base pool size for more sample and changing the MUTATOR setting to incrementation instead of reset because we don't know the full length")


process(500,100)
