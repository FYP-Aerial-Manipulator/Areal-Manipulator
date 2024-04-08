"""
    difference based control of manipulator 
    minimum jerk trajectory is updated with every camera input
"""


import numpy as np
# import Manipulator
import inverse_kine 
import matplotlib.pyplot as plt

def coeff_mat(T):
    A = [[1,    0,     0,          0,      0,          0],
         [0,    1/T,   0,          0,      0,          0],
         [0,    0,     2/T**2,     0,      0,          0],
         [1,    1,     1,          1,      1,          1],
         [0,    1/T,   2/T,        3/T,    4/T,        5/T],
         [0,    0,     2/T**2,     6/T**2, 12/T**2,    20/T**2]]
    return np.array(A)

def main():
    #==============Manipulator definition==============
    pins = [2, 6, 8, 14]
    init_config = [75, 90,90, 90]
    # arm = Manipulator.Manipulator(3, pins, init_config)
    

    #==============Initial ==============
    # pos = arm.config
    pos = [90, 90, 90]
    vec = [0, 0, 0]
    acc = [0, 0, 0]

    run_time = 5    # seconds
    num_seg = 20    # number of segments
    delay = 0.01    # motor value update delay

    # Random angles generation representing varying camera inputs
    error = np.random.normal(0, 1, num_seg)
    angle1 = 10*np.ones(num_seg) + error
    error = np.random.normal(0, 1, num_seg)
    angle2 = 10*np.ones(num_seg) + error
    error = np.random.normal(0, 1, num_seg)
    angle3 = 20*np.ones(num_seg) + error


    plotvalues1 = []
    plotvalues2 = []
    plotvalues3 = []
    plotvel1 = []
    plotvel2 = []
    plotvel3 = []
    plotacc1 = []
    plotacc2 = []
    plotacc3 = []

    for i in range(num_seg):
        # text = input("Enter desired coordinate: ").split(' ')
        # user_input = [float(i) for i in text if i]
        # user_input = [10, 10, 20]
        user_input = [angle1[i], angle2[i], angle3[i]]
        final_config = inverse_kine.inverse_kine(user_input)
        B = np.array([pos, vec, acc, final_config, [0, 0, 0], [0, 0, 0]])
        T = run_time*(num_seg-i)/num_seg
        coeff = np.dot(np.linalg.inv(coeff_mat(T)), B)
        timeline = [[(t/T)**j for j in range(6)] for t in np.arange(0, run_time/num_seg, delay)]
        timeline = np.array(timeline)
        print(timeline.shape)

        # print(timeline)
        
        traj = np.dot(timeline, coeff)
        # print(traj.shape)

        # arm.follow_trajectory(traj, delay)
        

        for i in range(len(traj)):
            # print("following:", traj[i])
            plotvalues1.append(traj[i][0])
            plotvalues2.append(traj[i][1])
            plotvalues3.append(traj[i][2])



        t = run_time/num_seg
        temp_config = [[(t/T)**j for j in range(6)], 
                       [j*(t**(j-1))/T**j for j in range(6)],
                       [0, 0, 2/T**2, 6*t/T**3, 12*t**2/T**4, 20*t**3/T**5]
                       ]
        temp_config = np.array(temp_config)
        end_state = np.dot(temp_config, coeff)
        # print(state)
        pos = end_state[0]
        vec = end_state[1]
        acc = end_state[2]


        velocities = [[j*(t**(j-1))/T**j for j in range(6)] for t in np.arange(0, run_time/num_seg, delay)]
        velocities = np.dot(velocities, coeff)
        for i in range(len(velocities)):
            plotvel1.append(velocities[i][0])
            plotvel2.append(velocities[i][1])
            plotvel3.append(velocities[i][2])

        accelerations = [[0, 0, 2/T**2, 6*t/T**3, 12*t**2/T**4, 20*t**3/T**5] for t in np.arange(0, run_time/num_seg, delay)]
        accelerations = np.dot(accelerations, coeff)
        for i in range(len(accelerations)):
            plotacc1.append(accelerations[i][0])
            plotacc2.append(accelerations[i][1])
            plotacc3.append(accelerations[i][2])

    
    # plt.plot(plotvalues1)
    # plt.plot(plotvalues2)
    plt.plot(plotvalues3)
    # plt.plot(plotvel1)
    # plt.plot(plotvel2)
    plt.plot(plotvel3)
    # plt.plot(plotacc1)
    # plt.plot(plotacc2)
    plt.plot(plotacc3)

    plt.legend(['pos', 'vel', 'acc'])
    plt.show()

    #==================================================

if __name__=="__main__":
    main()