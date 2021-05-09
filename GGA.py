#################################################
# ------- Generic Genetic Algorithm : GGA ------#
#   Author : Antoine Zellmeyer                  #
#   Mail : antoine.zellmeyer@epita.fr           #
#   PyVersion : Python 3                        #
#################################################

import math
import random

class Population:
    """
    Different Generation Option :
    """
    def RandomInit(self, poolsize, rangeLow, rangeHigh, NoFloat=False):
        pool = []
        if not NoFloat:
            gen = random.uniform
        else:
            gen = random.randint
        for _ in range(poolsize):
            pool.append(gen(rangeLow,rangeHigh))
        return pool


class CrossOver:
    """
    Different CrossOver Option :
    TODO : optimize by yielding results instead of creating a new array
    """
    def OnePoolSelect(self,pool):
        return pool

    def OnePoint(self, poolone,pooltwo):
        x = random.randint(0,len(poolone))
        pool = []
        for y in range(len(poolone)):
            if y < x:
                 pool.append(poolone[y])
            else:
                pool.append(pooltwo[y])
        return pool

    def MultiPoint(self, poolone,pooltwo,nb_points):
        pts = [random.randint(0,len(poolone)) for _ in range(nb_points)]
        pts.sort()
        if nb_points == 0:
            pts = [-10000000]
        pool = []
        k = 0
        ref = poolone
        for y in range(len(poolone)):
            if k < len(pts) and y < pts[k]:
                if (k%2 == 0):
                    ref = pooltwo
                else:
                    ref = poolone
                k+=1
            pool.append(ref[y])
        return pool

class Mutation:
    """
    Different Mutation Option
    """
    def NoMutation(self, pool):
        return pool
    def RandomReset(self, pool, chance, BornesReset):
        """
        >pool : array of element
        >chance : float between 0 and 1
        >BornesReset : array with two element representing the range of reset
        """
        for i in range(len(pool)):
            if random.uniform(0,1) < chance:
                pool[i] = random.uniform(BornesReset[0],BornesReset[1])
        return pool

# Constant Class Access
MUTATOR = Mutation()
CROSS = CrossOver()
POP = Population()
