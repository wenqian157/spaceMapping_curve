# speed difference

import time
import math
import random

def math_sqrt(num_list):
    for i in num_list:
        math.sqrt(i)

def arit_sqrt(num_list):
    for i in num_list:
        i ** .5

def math_static(value, count):
    for i in range(count):
        math.sqrt(value)

def math_2(count):
    for i in range(count):
        math.sqrt(2.0)

rnd_nrs = [random.random()* 100000 for i in range(100000)]

start_time = time.time()
math_sqrt(rnd_nrs)
print("math duration:{}".format(time.time() - start_time))

start_time = time.time()
arit_sqrt(rnd_nrs)
print("arit duration:{}".format(time.time() - start_time))

start_time = time.time()
math_static(3.0, 100000)
print("math 3.0 duration:{}".format(time.time() - start_time))

start_time = time.time()
math_static(2, 100000)
print("math 2 duration:{}".format(time.time() - start_time))

start_time = time.time()
math_2(100000)
print("math 2_2 duration:{}".format(time.time() - start_time))