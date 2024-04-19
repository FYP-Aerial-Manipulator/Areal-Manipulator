from math import sqrt
import Manipulator
import inverse_kine 
import trajectory_gen
from minimum_jerk_trajectory import minimum_jerk_trajectory
from time import sleep
import numpy as np

pins = [2, 6, 8, 14]
init_config = [140, 150,40, 90]#140

arm = Manipulator.Manipulator(3, pins, init_config)

while True:
    arm.open_grip()
    _ = input()

    arm.close_grip()
    _ = input()

