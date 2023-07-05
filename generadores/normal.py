import math
import random


def normal(media, v):
    rnd1 = random.random()
    rnd2 = random.random()
    n1 = (((math.sqrt(-2 * math.log(rnd1))) * math.cos(2 * math.pi * rnd2)) * v) + media
    n2 = (((math.sqrt(-2 * math.log(rnd1))) * math.sin(2 * math.pi * rnd2)) * v) + media
    return n1, n2
