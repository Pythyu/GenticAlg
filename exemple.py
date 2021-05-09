import math
import random
from GGA import *

########### Affine function ###############

def mystery_func():
    a = random.randint(-100,100)
    b = random.randint(-100,100)
    print("Generated func : ",[a,b])
    return lambda x: a*x + b

func = mystery_func()

def gen_rnd_a_b():
    return [random.randint(-10,10),random.randint(-10,10)]


####################  GGA Application ##################

def poolFitness(elem):
    score = 0
    tmp = lambda x: elem[0]*x + elem[1] # elem contains a and b : [a,b]
    for x in range(-100,100):
        s = 10 - abs(func(x/10) - tmp(x/10))
        if s > 0:
            score += s
    return score

def genFromParent(p1,p2):
    pool = CROSS.MultiPoint(p1,p2,random.randint(0,2))
    pool = MUTATOR.RandomReset(pool,0.1,[-100,100])
    return pool

def process(nb_pool, iteration=100):
    pools = [gen_rnd_a_b() for _ in range(nb_pool)]
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

        if i%50 == 0:
            print("Iteration ", i, " >> TOP 2 : ")
            print(mx)
            print(mx2)
            print(" --===--")
        pools = [genFromParent(mx[1],mx2[1]) for _ in range(nb_pool)]

    print("result : ", mx[1])

process(500,200)


def generer_enfant_depuis_parent(parent1,parent2,nombre_elem):
    # Générations de la nouvelle population à partir des deux parents en crossover
    nouvelle_pop = generer_enfants_par_crossover(parent1,parent2,nombre_elem))
    # Mutations des enfants des parents pour développer une nouvelle population diverse
    nouvelle_pop = mutation_de_population(nouvelle_pop)
    return nouvelle_pop

def genetic_process(nombre_elem, iteration=100):
    # Générer la population initiale
    pools = generer_population_initial(nombre_elem)
    for i in range(iteration):
        scores = []
        for pool in pools:
            v = evaluer(pool) # fonction d'évaluation
            scores.append(v)
        #  Sélections des deux parents
        best1, best2 = recuperer_deux_meilleurs(scores, pools)
        #  Générations des enfants => redéfinition de la population
        pools = generer_enfant_depuis_parent(best1,best2,nombre_elem)

    print("meilleur résulat : ", best1)
