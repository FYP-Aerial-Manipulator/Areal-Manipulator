from math import sqrt
import Manipulator
import inverse_kine 
import trajectory_gen
from time import sleep


def main():

    # take input
    # user_text = input("Enter desired coordinate: ").split(' ')  # x y z coordinates
    # des_coord = [float(i) for i in user_text if i]
    des_coord = [10, 10, 20]
    print("Entered coordinate:", des_coord)

    pins = [0, 1, 2, 3]
    init_config = [90, 90, 90, 90]

    arm = Manipulator.Manipulator(3, pins, init_config)

    # generate via point
    r = sqrt(des_coord[0]**2 + des_coord[1]**2)   # sqrt(x**2 + y**2)
    via = [des_coord[0]*(r-4)/r, des_coord[1]*(r-4)/r, des_coord[2]]  # via point 4cm from desired coordinate
    via_config = inverse_kine.inverse_kine(via)

    # final destination
    req_config = inverse_kine.inverse_kine(des_coord)

    # trajectory generation
    time_dur = 5
    freq = 5
    time_at_via = 3.5
    _, traj = trajectory_gen.trajectory_gen(arm.config, via_config, req_config, time_at_via, time_dur, freq) 

    # follow trajectory in class function
    delay = 1/freq
    arm.follow_trajectory(traj, delay)
    arm.close_grip()
    print("Object grapped!")
    sleep(1)

    # lifting object
    rev_time_dur = 2
    _, rev_traj = trajectory_gen.rev_trajectory_gen(arm.config, init_config, rev_time_dur, freq)
    arm.follow_trajectory(rev_traj, delay)




if __name__ == "__main__":
    main()