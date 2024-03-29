from math import sqrt
import Manipulator
import inverse_kine 
import trajectory_gen
from time import sleep


def main():

    pins = [2, 6, 8, 14]
    init_config = [75, 90,90, 90]#5

    arm = Manipulator.Manipulator(3, pins, init_config)
    # take input
    user_text = input("Enter desired coordinate: ").split(' ')  # x y z coordinates
    des_coord = [float(i) for i in user_text if i]
    # des_coord = [20, -10, 20]
    print("Entered coordinate:", des_coord)
    sleep(2)
    # generate via point
    r = sqrt(des_coord[0]**2 + des_coord[1]**2)   # sqrt(x**2 + y**2)
    via = [des_coord[0]*(r-4)/r, des_coord[1]*(r-4)/r, des_coord[2]]  # via point 4cm from desired coordinate
    via_config = inverse_kine.inverse_kine(via)

    # final destination
    req_config = inverse_kine.inverse_kine(des_coord)
    print("anlges for all joints: ", req_config)

    # trajectory generation
    time_dur = 6
    freq = 50
    time_at_via = 4
    _, traj = trajectory_gen.trajectory_gen(arm.config, via_config, req_config, time_at_via, time_dur, freq) 

    # follow trajectory in class function
    delay = 1/freq
    _ = input("Press Enter to follow the desired coordinate!!!")
    arm.follow_trajectory(traj, delay)
    sleep(2)
    arm.close_grip()
    sleep(2)
    # print("Object grapped!")
    

    # lifting object
    rev_time_dur = 6
    _, rev_traj = trajectory_gen.rev_trajectory_gen(arm.config, init_config, rev_time_dur, freq)
    _ = input("Press Enter to return home!!!")
    arm.follow_trajectory(rev_traj, delay)




if __name__ == "__main__":
    main()