import numpy as np
from fact import fact
import matplotlib.pyplot as plt

# Minimum snap trajectroy generation
def traj_gen(waypoints=[0,1,2,3], timelapse=[0,2,4,6]):

    # number of waypoints
    n = len(timelapse) - 1

    # number of order of polynomials
    p = 7 # odd number almost always
    k = (p-1)//2 

    waypoints = np.array(waypoints)
    timelapse = np.array(timelapse)

    # time periods
    T = np.array([timelapse[i+1]-timelapse[i] for i in range(n)]) 
    # print(T)


    A = np.zeros((8*n,8*n))

    ################## FIRST CONDITION ############### Pi(S_i-1) = W_i-1
    for i in range(n):
        A[i][8*i] = 1

    
    ################## SECOND CONDITION ############### 
    for i in range(n):
        A[i+n][8*i:8*(i+1)] = np.ones(8)

    ################## THIRD CONDITION ############### 
    for i in range(1, k + 1):
        A[i + 2*n - 1][i] = fact(i)/(T[0]**i)

    ################## FORTH CONDITION ############### 
    for i in range(k):
        A[i + 2*n + k][-7 + i :] = [fact(j)/fact(j-i-1)/T[n-1]**(i+1) for j in range(i+1, p+1)]

    ################## FIFTH CONDITION ############### 
    for i in range(n-1):
        temp = np.append([j/T[i] for j in range(1, 8)], np.array([0, -1/T[i+1]]))
        A[i + 2*n + 2*k][8*i + 1 : 8*i + 10] = temp

    ################## SIXTH CONDITION ############### 
    temp_array = [i*(i-1) for i in range(2, 8)]
    for i in range(n-1):
        a= temp_array/T[i]**2
        b= [0, 0, -2/T[i+1]**2 ]
        temp = np.append(a, b)
        A[i + 3*n + 2*k -1][8*i + 2 : 8*i + 11] = temp

    ################## SEVENTH CONDITION ############### 
    temp_array = [i*(i-1)*(i-2) for i in range(3, 8)]
    for i in range(n-1):
        a= temp_array/T[i]**3
        b= [0, 0, 0, -fact(3)/T[i+1]**3]
        temp = np.append(a, b)
        A[i + 4*n + 2*k -2][8*i + 3 : 8*i + 12] = temp

    ################## EIGHT CONDITION ############### 
    temp_array = [fact(i)/fact(i-4) for i in range(4, 8)]
    for i in range(n-1):
        a= temp_array/T[i]**4
        b= [0, 0, 0, 0, -fact(4)/T[i+1]**4 ]
        temp = np.append(a, b)
        A[i + 5*n + 2*k -3][8*i + 4 : 8*i + 13] = temp

    
    ################## ninth CONDITION ############### 
    temp_array = [fact(i)/fact(i-5) for i in range(5, 8)]
    for i in range(n-1):
        a= temp_array/T[i]**5
        b= [0, 0, 0, 0, 0, -fact(5)/T[i+1]**5 ]
        temp = np.append(a, b)
        A[i + 6*n + 2*k -4][8*i + 5 : 8*i + 14] = temp

    ################## ninth CONDITION ############### 
    temp_array = [fact(i)/fact(i-6) for i in range(6, 8)]
    for i in range(n-1):
        a= temp_array/T[i]**6
        b= [0, 0, 0, 0, 0, 0, -fact(6)/T[i+1]**6 ]
        temp = np.append(a, b)
        A[i + 7*n + 2*k -5][8*i + 6 : 8*i + 15] = temp
    


    ###########  B  matrix #######################
    B = np.zeros((8*n))

    for i in range(n):
        B[i] = waypoints[i]
    for i in range(n):
        B[n+i] = waypoints[i+1]   

    B.reshape((8*n,1))
    alpha = np.dot(np.linalg.inv(A), B)
    # print(A)
    return alpha


#################### INPUTS HERE ###################
# points to follow and the time (desired trajectory)
waypoints = [0, 10, 10, 12, 15]
timelapse = [0, 5, 6, 8, 10]
# waypoints = np.arange(0,7)
# waypoints = np.zeros(6)
# timelapse = np.arange(0,13,2)
###################################################

n = len(timelapse)-1
# print(waypoints, timelapse)

# coefficients for the polynomials
alpha = traj_gen(waypoints, timelapse)
alpha = alpha.reshape((n,8))
# print(len(alpha))



time = np.array([])
Ppos = np.array([]) # trajectory position
Pvel = np.array([])
Pacc = np.array([])
Pjer = np.array([])
Psnap = np.array([])

# generating time and trajectory
for i in range(n):
    Ss = timelapse[i]
    Se = timelapse[i+1]
    T = Se-Ss
    print(Ss, Se)
    timeslice = np.arange(Ss, Se, 0.1)

    # position calculation
    constantpos = [((t-Ss)/(T))**j for t in timeslice for j in range(8)]
    constantpos = np.array(constantpos)
    constantpos = constantpos.reshape((len(timeslice),8))
    Pposslice = np.dot(constantpos, alpha[i])
    Ppos = np.append(Ppos, Pposslice)

    # velocity calculation
    constantvel = [j/(T)*((t-Ss)/(T))**(j-1) for t in timeslice for j in range(8)]
    constantvel = np.array(constantvel)
    constantvel = constantvel.reshape((len(timeslice),8))
    constantvel[:][0]=0
    Pvelslice = np.dot(constantvel, alpha[i])
    # if Se==2 or Se==4:
    #     print(Pvelslice)
    Pvel = np.append(Pvel, Pvelslice)


    # acceleration calculation
    constantacc = [j*(j-1)/(T)**2*((t-Ss)/(T))**(j-2) for t in timeslice for j in range(8)]
    constantacc = np.array(constantacc)
    constantacc = constantacc.reshape((len(timeslice),8))
    constantacc[:][0:2]=0
    Paccslice = np.dot(constantacc, alpha[i])
    Pacc = np.append(Pacc, Paccslice)


    # jerk calculation
    constantjer = [j*(j-1)*(j-2)/(T)**3*((t-Ss)/(T))**(j-3) for t in timeslice for j in range(8)]
    constantjer = np.array(constantjer)
    constantjer = constantjer.reshape((len(timeslice),8))
    constantjer[:][0:3]=0
    Pjerslice = np.dot(constantjer, alpha[i])
    Pjer = np.append(Pjer, Pjerslice)
    

    # snap calculation
    constantsnap = [j*(j-1)*(j-2)*(j-3)/(T)**4*((t-Ss)/(T))**(j-4) for t in timeslice for j in range(8)]
    constantsnap = np.array(constantsnap)
    constantsnap = constantsnap.reshape((len(timeslice),8))
    constantsnap[:][0:4]=0
    Psnapslice = np.dot(constantsnap, alpha[i])
    Psnap = np.append(Psnap, Psnapslice)


    time = np.append(time,timeslice)

fig, axs = plt.subplots(2,3)
axs[0,0].plot(time, Ppos, 'b')
axs[0,0].plot(timelapse, waypoints, 'rx')
axs[0,0].set_title("position")
axs[0,1].plot(time, Pvel, 'b')
axs[0,1].set_title("velocity")
axs[0,2].plot(time, Pacc, 'b')
axs[0,2].set_title("acceleration")
axs[1,0].plot(time, Pjer, 'b')
axs[1,0].set_title("jerk")
axs[1,1].plot(time, Psnap, 'b')
axs[1,1].set_title("snap")
plt.show()