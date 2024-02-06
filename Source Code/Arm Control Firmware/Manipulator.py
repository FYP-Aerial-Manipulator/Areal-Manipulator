from time import sleep
import numpy as np

def set_motor(motor__pin_no, angle):
    pass


class Manipulator:
    def __init__(self, dof, pins, init_config):
        self.dof = dof
        self.pins = pins
        self.config = init_config
        self.write_config(init_config)
        self.open_grip()
    
    def write_config(self, config):
        for i in range(self.dof):
            set_motor(self.pins[i], config[i])
        self.config = config
    
    def close_grip(self):
        set_motor(self.pins[3], 40)

    def open_grip(self):
        set_motor(self.pins[3], 30)

    def follow_trajectory(self, traj, delay):
        trajlen = len(traj[0])
        for i in range(trajlen):
            safe_angles = self.safe_limits(traj[:,i])
            self.write_config(safe_angles)
            print("following:", safe_angles)

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

    