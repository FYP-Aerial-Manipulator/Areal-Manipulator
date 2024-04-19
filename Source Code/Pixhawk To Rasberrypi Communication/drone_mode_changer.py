from dronekit import connect, VehicleMode
import time

# Connect to the Pixhawk using serial connection
vehicle = connect('/dev/ttyACM0', baud=115200, wait_ready=True)

# Change the mode to "GUIDED"
new_mode = VehicleMode("STABILIZE") #STABILIZE ,GUIDED ,LOITER
vehicle.mode = new_mode

time.sleep(1) 
# Print the updated Pixhawk mode
print("Updated Vehicle Mode:", vehicle.mode.name)

# Close the connection when done
vehicle.close()
