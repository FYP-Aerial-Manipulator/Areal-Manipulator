from math import pi, sqrt, atan2, acos, degrees, sqrt
# import math

def inverse_kine(des_coord):
    x = des_coord[0]
    y = des_coord[1]
    z = des_coord[2]

    l1 = 11  # cm
    l2 = 19 # cm
    r = sqrt(x**2 + y**2)
    a = sqrt(x**2 + y**2 + z**2)

    angle_1 = degrees(atan2(x, -y)) - 17
    angle_2 = degrees(atan2(z, r) + acos((l1**2 + a**2 - l2**2)/(2*a*l1))) -7
    angle_3 = degrees(acos((l1**2 + l2**2 - a**2)/(2*l1*l2)))
    

    return [angle_1, angle_2, angle_3]


if __name__ == "__main__":
    while True:
        try:
            #user_text = input("insert desired coordinate with space seperated: ").split(' ')  # x y z coordinates
            #des_coord = [float(i) for i in user_text if i]
            des_coord = [13.4, 1.2, 21.3]
            print(inverse_kine(des_coord))
        except KeyboardInterrupt:
            break
