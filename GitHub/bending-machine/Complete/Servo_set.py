from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyAMA0", baudrate=1000000)

dynamixel_id = 1
x=1.0

while 1:

    print("set degree :")
    inp=input()

    x=float(inp)-150.0
    if x>=-150 and x<=150:
        print(f"Go to {x}")
        serial_connection.goto(dynamixel_id, x, speed=50, degrees=True)
        time.sleep(2)    # Wait 1 second



# Close the serial connection
serial_connection.close()