import math
import random


def poisson(lmbd):
    p, x = 1, -1
    a = math.pow(math.e, -lmbd)
    while p >= a:
        rnd = random.random()
        p = p * rnd
        x += 1
    return x
