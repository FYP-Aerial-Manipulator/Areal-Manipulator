from math import sqrt
import Manipulator
import inverse_kine 
import trajectory_gen
from minimum_jerk_trajectory import minimum_jerk_trajectory
from time import sleep
import numpy as np
def main():

    pins = [2, 6, 8, 14]
    init_config = [140, 150,40, 90]#140

    arm = Manipulator.Manipulator(3, pins, init_config)
    # take input
    with open('/home/pi/Desktop/Codes/Object Tracking/Object_3D_Cordinate.txt', 'r') as file:
        for line in file:
            # Split the line into individual coordinate values
            coordinates = line.strip().split()
            x = float(coordinates[0])
            y = float(coordinates[1])
            z = float(coordinates[2])
            #print(x, y, z)
    
    #user_text = input("Enter desired coordinate: ").split(' ')  # x y z coordinates
    #des_coord = [float(i) for i in user_text if i]
    des_coord = [x, y, z]
#     des_coord = [14, 0, 26]
    # Read coordinates from file
        
    print("Entered coordinate:", des_coord)
    sleep(0.5)
    # generate via point
    
    r = sqrt(des_coord[0]**2 + des_coord[1]**2)   # sqrt(x**2 + y**2)
    via = [des_coord[0]*(r-6)/r, des_coord[1]*(r-6)/r, des_coord[2]]  # via point 4cm from desired coordinate
    via_config = inverse_kine.inverse_kine(via)

    # print(via_config)
    # print(type(via_config))
    

    # final destination
    req_config = inverse_kine.inverse_kine(des_coord)
  
    print("anlges for all joints: ", req_config)

    # trajectory generation
    via_time = 3
    time_dur = 4
    delay = 0.0018
    # freq = 50
    # time_at_via = 4

    _, via_traj = minimum_jerk_trajectory(arm.config[:3], via_config, via_time, delay)
    _, rest_traj = minimum_jerk_trajectory(via_config, req_config, time_dur - via_time, delay)
    # print(via_traj[0])
    # print(rest_traj[0])
    traj = np.concatenate((via_traj, rest_traj))
    # print(traj[0])
    # follow trajectory in class function
    # delay = 1/freq
    # _ = input("Press Enter to follow the desired coordinate!!!")
    arm.follow_trajectory(traj, delay)
    sleep(0.5)
    arm.close_grip()
    sleep(0.5)
    # print("Object grapped!")
    #_ = input("Press Enter to follow the desired coordinate!!!")
    

    # lifting object
    rev_time_dur = 4
    _, rev_traj = minimum_jerk_trajectory(arm.config[:3], init_config[:3], rev_time_dur, delay)
    # _ = input("Press Enter to return home!!!")
    arm.follow_trajectory(rev_traj, delay)




if __name__ == "__main__":
    main()