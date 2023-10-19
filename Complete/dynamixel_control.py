# Define the serial port and baud rate
port = "/dev/ttyUSB1"  # Update with the correct port
baud_rate = 1000000  # Default baud rate for Dynamixel AX-12A


from pyax12.connection import Connection

# Define the serial port and baud rate
port = "/dev/ttyUSB0"  # Change this to the correct port for your setup
baud_rate = 1000000  # Default baud rate for Dynamixel AX-12A

# Create a connection to the serial port
serial_connection = Connection(port=port, baudrate=baud_rate)

# Set the ID of the servo you want to control
servo_id = 1  # Change this to the ID of your AX-12A servo

# Define the target position (angle or position value)
target_position = 512  # Adjust this value as needed

# Send the goal position command to the servo
serial_connection.goto(servo_id, target_position)

# Close the serial connection when done
serial_connection.close()
