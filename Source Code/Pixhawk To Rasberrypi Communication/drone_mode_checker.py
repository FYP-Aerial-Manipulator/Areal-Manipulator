from dronekit import connect, VehicleMode
import time

# Connect to the Pixhawk using serial connection
vehicle = connect('/dev/ttyACM0', baud=115200, wait_ready=True)

# Do something with the vehicle
print("Connected to Pixhawk")
#print("Vehicle Firmware Version:", vehicle.version)
time.sleep(1) 

# Print the current Pixhawk mode
print("Current Vehicle Mode:", vehicle.mode.name)

# Write the current vehicle mode to a text file
with open("drone_mode.txt", "w") as file:
    file.write(vehicle.mode.name)

# Close the connection when done
vehicle.close()

