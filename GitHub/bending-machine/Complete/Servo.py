from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyAMA0", baudrate=1000000)

dynamixel_id = 1


while 1:


    print("Go to 90")
    serial_connection.goto(dynamixel_id, 90, speed=50, degrees=True)
    time.sleep(8)    # Wait 1 second

    print("Go to -90")
    serial_connection.goto(dynamixel_id, -90, speed=512, degrees=True)
    time.sleep(3)    # Wait 1 second


# Close the serial connection
serial_connection.close()