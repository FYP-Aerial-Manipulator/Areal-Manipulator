import numpy as np
import matplotlib.pyplot as plt



def trajectory_gen(ini, via, req, tvia, dur, freq):
    """
    simple shorteest distance trajectory generation
    """
    delay = 1/freq
    timeline = np.arange(0, dur, delay)
    midpoint = int((tvia-0)*freq)
    traj = np.zeros((3, len(timeline))) # trajectory for all joints

    for i in range(3):
        traj[i][:midpoint] = np.linspace(ini[i], via[i], midpoint+1)[:-1]
        traj[i][midpoint:] = np.linspace(via[i], req[i], len(timeline)-midpoint)
    
    if len(timeline) == len(traj[0]):
        return timeline, traj
    else:
        print("error occured in trajectory generation")


def rev_trajectory_gen(ini, req, dur, freq):
    delay = 1/freq
    timeline = np.arange(0, dur, delay)
    traj = np.zeros((3, len(timeline)))

    for i in range(3):
        traj[i] = np.linspace(ini[i], req[i], len(timeline))
        
    if len(timeline) == len(traj[0]):
        return timeline, traj
    else:
        print("error occured in trajectory generation")


if __name__ == "__main__":
    # testing the function
    
    mytimeline, mytraj = trajectory_gen([0,0,0], [30,40,50], [35,45, 55], 3, 6, 10)
    # mytimeline, mytraj = rev_trajectory_gen([35,45, 55], [90, 90, 90], 2, 10)

    # print()
    plt.plot(mytimeline, mytraj[2])
    plt.plot(mytimeline, mytraj[1])
    plt.plot(mytimeline, mytraj[0])
    plt.show()