from time import sleep
import numpy as np
from adafruit_servokit import ServoKit

class Manipulator:
    def __init__(self, dof, pins, init_config):
        self.dof = dof
        self.pins = pins

        # Initialize the PCA9685 module and servo kit
        self.kit = ServoKit(channels=16)
        # Set the frequency of the PWM signal
        for i in self.pins:
            self.kit.servo[i].set_pulse_width_range(500, 2500)
        # print("manipulator initiated!!!")
        
        self.config = init_config
        self.write_config(init_config)
        sleep(3)   # time to acquire initial position
        self.open_grip()


    
    def write_config(self, config):
        for i in range(self.dof):
            self.move_servo(self.pins[i], config[i])
        self.config = config
    
    def close_grip(self):
        self.move_servo(self.pins[3], 80)
        print("gripper closed!")

    def open_grip(self):
        self.move_servo(self.pins[3], 30)
        print("gripper opened!")

    def follow_trajectory(self, traj, delay):
        trajlen = traj.shape[1]
        # print("length of the trajectory: ", trajlen)
        for i in range(trajlen):
            safe_angles = self.safe_limits(traj[:,i])
            self.write_config(safe_angles)
            # print("following:", safe_angles)

            sleep(delay)
    
    def safe_limits(self, degrees):
        out_degrees = degrees.copy()

        # Joint 1 limits
        out_degrees[0] = max(0, min(180, out_degrees[0]))

        # Joint 2 limits
        out_degrees[1] = max(30, min(160, out_degrees[1]))

        # Joint 3 limits
        out_degrees[2] = max(60, min(160, out_degrees[2]))

        if np.any(out_degrees != degrees):
            print("Warning!!! Joint angle trimmed!!!")
            print("Original angles:", degrees)
            print("Trimmed angles:", out_degrees)

        return out_degrees
    
    def move_servo(self, motor__pin_no, angle):
        self.kit.servo[motor__pin_no].angle = angle
        # sleep(1)  # Give the servo some time to move

    