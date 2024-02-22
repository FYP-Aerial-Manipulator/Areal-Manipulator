from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

# Create a custom pin-factory to fix servo jitter
pigpio_factory = PiGPIOFactory()

# Specify the GPIO pin and use the custom pin-factory
servo = Servo(12, pin_factory=pigpio_factory)

while True:
    try:
        # Get user input for the servo angle
        angle = float(input("Enter servo angle (-90 to 90 degrees, 0 for center): "))
        
        # Clamp the angle within the valid range
        angle = max(-90, min(90, angle))
        
        # Set the servo to the specified angle
        servo.value = angle / 90.0  # Convert angle to a value between -1 and 1
        print(f"Set servo angle to {angle} degrees")
        
        sleep(1)  # Sleep for 1 second
        
    except ValueError:
        print("Invalid input. Please enter a valid number.")
