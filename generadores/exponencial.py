import math
import random


def exponencial(media):
    rnd = random.random()
    n = -media * math.log(1 - rnd)
    return n


def exponencial2(media):
    rnd = random.random()
    n = -media * math.log(1 - rnd)
    return rnd, n
